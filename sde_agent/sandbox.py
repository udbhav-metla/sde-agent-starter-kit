import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from pathlib import Path
from .security import Fault, safe_path


def run_checks(settings, files, trusted_fixture=False, cancelled=lambda: False):
    """Only shipped fixture code runs on host. All external code requires Docker."""
    docker = shutil.which('docker')
    if not trusted_fixture and not docker:
        raise Fault('TOOL_UNAVAILABLE', 'Docker is required to run repository code. No host-shell fallback is permitted.', 503)
    with tempfile.TemporaryDirectory(prefix='sde-', dir=settings.data_dir) as tmp:
        root = Path(tmp)
        for path, content in files.items():
            target = root / safe_path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
        name = 'sde-' + uuid.uuid4().hex
        if trusted_fixture:
            cmd = [sys.executable, '-I', '-B', '-m', 'unittest', 'discover', '-s', str(root), '-v']
        else:
            cmd = [docker, 'run', '--rm', '--pull=never', '--name', name, '--network=none', '--memory=256m', '--cpus=1', '--pids-limit=32', '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges', '--user=65534:65534', '--tmpfs=/tmp:rw,noexec,nosuid,size=64m', '--mount', f'type=bind,source={root},target=/workspace,readonly', '-w', '/workspace', settings.docker_image, 'python', '-I', '-B', '-m', 'unittest', 'discover', '-s', '/workspace', '-v']
        env = {k: os.environ[k] for k in ('SYSTEMROOT', 'WINDIR', 'PATH', 'TEMP', 'TMP', 'DOCKER_HOST', 'DOCKER_CONTEXT', 'DOCKER_CONFIG') if k in os.environ}
        start = time.monotonic()
        reason = None
        # Disk-backed bounded capture avoids pipe deadlocks and unbounded RAM.
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            proc = subprocess.Popen(cmd, cwd=root, env=env, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, shell=False)
            try:
                while proc.poll() is None:
                    if cancelled():
                        reason = 'CANCELLED'
                    elif time.monotonic() - start > settings.test_timeout:
                        reason = 'TIMEOUT'
                    elif os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > 1024 * 1024:
                        reason = 'OUTPUT_LIMIT'
                    if reason:
                        proc.kill()
                        break
                    time.sleep(0.05)
                proc.wait(timeout=5)
            finally:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=5)
                if not trusted_fixture:
                    subprocess.run([docker, 'rm', '-f', name], capture_output=True, timeout=10, check=False)
            stdout.seek(0)
            stderr.seek(0)
            out = stdout.read(65536).decode('utf-8', errors='replace')
            err = stderr.read(65536).decode('utf-8', errors='replace')
        import re
        count = re.search(r'Ran (\d+) tests?', out + err)
        count = int(count[1]) if count else None
        # A zero exit with zero/no discovered tests is never verification.
        return dict(command='python -I -B -m unittest discover -s /workspace -v', stdout=out, stderr=err, exit_code=proc.returncode, tests=count, passed=proc.returncode == 0 and bool(count) and not reason, error=reason, duration_seconds=round(time.monotonic() - start, 3), isolation='shipped fixture subprocess' if trusted_fixture else 'Docker: no network, non-root, read-only, 256 MB, 1 CPU, 32 PIDs')
