import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: Path(os.getenv('SDE_DATA_DIR', '.data')).resolve())
    token: str = field(default_factory=lambda: os.getenv('SDE_API_TOKEN') or secrets.token_urlsafe(32))
    repositories: tuple[str, ...] = field(default_factory=lambda: tuple(x.strip() for x in os.getenv('SDE_ALLOWED_REPOS', '').split(',') if x.strip()))
    github_token: str = field(default_factory=lambda: os.getenv('GITHUB_TOKEN', ''))
    github_write: bool = field(default_factory=lambda: os.getenv('SDE_GITHUB_WRITE', 'false').lower() == 'true')
    model_id: str = field(default_factory=lambda: os.getenv('BEDROCK_MODEL_ID', ''))
    region: str = field(default_factory=lambda: os.getenv('AWS_REGION', 'us-east-1'))
    approval_seconds: int = 600
    test_timeout: int = 45
    docker_image: str = field(default_factory=lambda: os.getenv('SDE_SANDBOX_IMAGE', 'python:3.12-slim'))

