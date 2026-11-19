"""Configuration for local Ollama runtime. Secrets never required for default run."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = val


_load_dotenv(ROOT / ".env")

# Local-only by default — do not point at cloud endpoints in demos.
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "24"))
REQUEST_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "300"))

# Web fetch: open sources only; SSRF blocked in security.py
ALLOW_WEB_FETCH = os.getenv("ALLOW_WEB_FETCH", "1") not in ("0", "false", "False")

# Optional allowlist (comma-separated suffixes). Empty = any public http(s) with SSRF guards.
WEB_ALLOW_SUFFIXES = [
    s.strip().lower()
    for s in os.getenv(
        "WEB_ALLOW_SUFFIXES",
        "megafon.ru,wikipedia.org,github.com,habr.com",
    ).split(",")
    if s.strip()
]
