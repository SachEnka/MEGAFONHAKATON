"""Path sandbox and SSRF guards — keep project data local and tools constrained."""
from __future__ import annotations

import ipaddress
import socket
from pathlib import Path
from urllib.parse import urlparse

from .config import ROOT, WEB_ALLOW_SUFFIXES


class SecurityError(Exception):
    pass


def resolve_in_repo(path: str | Path) -> Path:
    """Resolve path and ensure it stays inside the repository root."""
    raw = Path(path)
    candidate = (ROOT / raw).resolve() if not raw.is_absolute() else raw.resolve()
    root = ROOT.resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise SecurityError(f"Path outside repository sandbox: {path}") from exc
    # Block escaping via weird suffixes
    if any(part == ".." for part in Path(path).parts):
        # still ok if resolved inside; double-check
        candidate.relative_to(root)
    return candidate


def assert_writable_target(path: Path) -> None:
    """Disallow writing into .git or secrets-looking locations."""
    rel = path.relative_to(ROOT.resolve())
    parts = {p.lower() for p in rel.parts}
    blocked = {".git", ".env", "secrets"}
    if parts & blocked or rel.name.lower() in {".env", ".env.local"}:
        raise SecurityError(f"Write blocked for protected path: {rel}")


def _host_is_private(hostname: str) -> bool:
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise SecurityError(f"DNS resolve failed for {hostname}: {exc}") from exc
    for info in infos:
        ip_str = info[4][0]
        try:
            ip = ipaddress.ip_address(ip_str)
        except ValueError:
            continue
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
        ):
            return True
    return False


def validate_fetch_url(url: str) -> str:
    """Allow only http(s) to public hosts; optional suffix allowlist."""
    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise SecurityError("Only http/https URLs are allowed")
    host = (parsed.hostname or "").lower()
    if not host:
        raise SecurityError("URL has no host")
    if host in {"localhost", "127.0.0.1", "0.0.0.0", "::1"}:
        raise SecurityError("Localhost fetch blocked (SSRF)")
    if _host_is_private(host):
        raise SecurityError(f"Private/reserved IP blocked for host {host}")
    if WEB_ALLOW_SUFFIXES:
        ok = any(host == s or host.endswith("." + s) for s in WEB_ALLOW_SUFFIXES)
        if not ok:
            raise SecurityError(
                f"Host `{host}` not in WEB_ALLOW_SUFFIXES ({', '.join(WEB_ALLOW_SUFFIXES)}). "
                "Add suffix in .env if this open source is needed."
            )
    return url.strip()
