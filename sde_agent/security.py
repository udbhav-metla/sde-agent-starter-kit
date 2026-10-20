import hashlib
import json
import re
from pathlib import PurePosixPath


class Fault(Exception):
    def __init__(self, code, message, status=400):
        self.code, self.message, self.status = code, message, status
        super().__init__(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()


def redact(value, secrets=()):
    if isinstance(value, dict):
        return {k: ('[Redacted]' if re.fullmatch(r'(?i)(?:.*_)?(?:token|password|secret|authorization|api_key|access_key|secret_access_key)', k) else redact(v, secrets)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(x, secrets) for x in value]
    if not isinstance(value, str):
        return value
    for secret in secrets:
        if secret and len(secret) >= 4:
            value = value.replace(secret, '[Redacted]')
    value = re.sub(r'-----BEGIN [^-]*PRIVATE KEY-----.*?-----END [^-]*PRIVATE KEY-----', '[Redacted]', value, flags=re.S)
    value = re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]+|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9_-]{16,})\b', '[Redacted]', value)
    return re.sub(r'(?i)((?:password|api[_-]?key|secret|token|authorization)\s*[=:]\s*)[^\s,;]+', r'\1[Redacted]', value)


def safe_path(path):
    p = PurePosixPath(path)
    if not path or len(path) > 220 or p.is_absolute() or '..' in p.parts or '\\' in path or ':' in path or any(x.startswith('.') for x in p.parts):
        raise Fault('POLICY_DENIED', 'Unsafe or hidden repository path.', 403)
    if any(not re.fullmatch(r'[A-Za-z0-9_.-]+', x) for x in p.parts):
        raise Fault('POLICY_DENIED', 'Unsupported repository path.', 403)
    return path


def scoped(repository, settings):
    if repository != 'demo/empty-input' and repository not in settings.repositories:
        raise Fault('SCOPE_MISMATCH', 'Repository is outside SDE_ALLOWED_REPOS.', 403)

