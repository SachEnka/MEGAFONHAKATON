"""Sandboxed tools for the Strategist agent (local-cli inspired allowlist)."""
from __future__ import annotations

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

from .config import ALLOW_WEB_FETCH, ROOT
from .security import SecurityError, assert_writable_target, resolve_in_repo, validate_fetch_url

ToolFn = Callable[..., str]


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._skip = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip:
            t = data.strip()
            if t:
                self._chunks.append(t)

    def text(self) -> str:
        return "\n".join(self._chunks)


def tool_list_dir(path: str = ".") -> str:
    p = resolve_in_repo(path)
    if not p.exists():
        return f"ERROR: not found: {path}"
    if p.is_file():
        return f"FILE {p.relative_to(ROOT)} ({p.stat().st_size} bytes)"
    lines = []
    for child in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        kind = "dir" if child.is_dir() else "file"
        lines.append(f"{kind}\t{child.relative_to(ROOT)}")
    return "\n".join(lines) or "(empty)"


def tool_read_file(path: str, max_chars: int = 12000) -> str:
    p = resolve_in_repo(path)
    if not p.exists() or not p.is_file():
        return f"ERROR: file not found: {path}"
    text = p.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[:max_chars] + f"\n\n...[truncated, {len(text)} chars total]"
    return text


def tool_write_file(path: str, content: str) -> str:
    p = resolve_in_repo(path)
    assert_writable_target(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"OK wrote {p.relative_to(ROOT)} ({len(content)} chars)"


def tool_append_file(path: str, content: str) -> str:
    p = resolve_in_repo(path)
    assert_writable_target(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(content)
    return f"OK appended to {p.relative_to(ROOT)} ({len(content)} chars)"


def tool_grep(pattern: str, path: str = ".", max_hits: int = 40) -> str:
    root = resolve_in_repo(path)
    try:
        rx = re.compile(pattern)
    except re.error as exc:
        return f"ERROR: bad regex: {exc}"
    hits: list[str] = []
    files: list[Path]
    if root.is_file():
        files = [root]
    else:
        files = [f for f in root.rglob("*") if f.is_file()]
    for f in files:
        if any(part.startswith(".") and part not in {".cursor"} for part in f.relative_to(ROOT).parts):
            # skip hidden except we already limited; skip .git via resolve
            if ".git" in f.parts:
                continue
        if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pyc", ".zip"}:
            continue
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{f.relative_to(ROOT)}:{i}: {line[:200]}")
                    if len(hits) >= max_hits:
                        return "\n".join(hits)
        except OSError:
            continue
    return "\n".join(hits) if hits else "(no matches)"


def tool_web_fetch(url: str, max_chars: int = 10000) -> str:
    if not ALLOW_WEB_FETCH:
        return "ERROR: web fetch disabled (ALLOW_WEB_FETCH=0)"
    try:
        safe = validate_fetch_url(url)
    except SecurityError as exc:
        return f"ERROR: {exc}"
    req = Request(safe, headers={"User-Agent": "StrategistLocalAgent/0.1 (+local research; open sources)"})
    try:
        with urlopen(req, timeout=25) as resp:
            raw = resp.read()
            ctype = (resp.headers.get("Content-Type") or "").lower()
    except Exception as exc:  # noqa: BLE001
        return f"ERROR fetching {url}: {exc}"
    text = raw.decode("utf-8", errors="replace")
    if "html" in ctype or text.lstrip().lower().startswith("<!doctype") or "<html" in text[:200].lower():
        parser = _TextExtractor()
        try:
            parser.feed(text)
            text = parser.text()
        except Exception:  # noqa: BLE001
            text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    header = f"SOURCE: {safe}\n---\n"
    body = text[:max_chars] + (f"\n...[truncated {len(text)} chars]" if len(text) > max_chars else "")
    return header + body


def tool_run_project_cli(script: str, project_id: str, extra_args: str = "") -> str:
    """Allowlist: only tools/*.py helpers."""
    allowed = {
        "status.py",
        "validate_artifacts.py",
        "evidence_index.py",
        "cost_log.py",
        "analyze_table.py",
        "compare_baseline.py",
    }
    name = Path(script).name
    if name not in allowed:
        return f"ERROR: script not allowlisted. Allowed: {sorted(allowed)}"
    script_path = ROOT / "tools" / name
    if not script_path.exists():
        return f"ERROR: missing {script_path}"
    args = [sys.executable, str(script_path), project_id]
    if extra_args.strip():
        # no shell; split on spaces simply
        args.extend(extra_args.split())
    try:
        proc = subprocess.run(
            args,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except Exception as exc:  # noqa: BLE001
        return f"ERROR running CLI: {exc}"
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return f"exit={proc.returncode}\n{out[:8000]}"


def tool_ask_user(question: str) -> str:
    print("\n=== HUMAN GATE ===")
    print(question)
    print("==================")
    try:
        answer = input("Your answer (or empty to skip): ").strip()
    except EOFError:
        answer = ""
    return answer or "(no answer — continue with explicit gap)"


HANDLERS: dict[str, ToolFn] = {
    "list_dir": tool_list_dir,
    "read_file": tool_read_file,
    "write_file": tool_write_file,
    "append_file": tool_append_file,
    "grep": tool_grep,
    "web_fetch": tool_web_fetch,
    "run_project_cli": tool_run_project_cli,
    "ask_user": tool_ask_user,
}

# OpenAI/Ollama tool schemas
SCHEMAS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List files/dirs inside the repository sandbox.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string", "description": "Relative path"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file from the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "max_chars": {"type": "integer"},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write/overwrite a file inside the repo (not .env/.git).",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "append_file",
            "description": "Append text to a file inside the repo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Regex search in repository text files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string"},
                    "max_hits": {"type": "integer"},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": "Fetch an allowlisted public http(s) page (open sources). SSRF blocked.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "max_chars": {"type": "integer"},
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_project_cli",
            "description": "Run allowlisted tools/*.py helper (status, validate, analyze_table, ...).",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {"type": "string"},
                    "project_id": {"type": "string"},
                    "extra_args": {"type": "string"},
                },
                "required": ["script", "project_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_user",
            "description": "Human gate: ask the product lead a blocking question (options choice, etc.).",
            "parameters": {
                "type": "object",
                "properties": {"question": {"type": "string"}},
                "required": ["question"],
            },
        },
    },
]


def dispatch(name: str, arguments: dict[str, Any]) -> str:
    fn = HANDLERS.get(name)
    if not fn:
        return f"ERROR: unknown tool {name}"
    try:
        return str(fn(**arguments))
    except TypeError as exc:
        return f"ERROR bad arguments for {name}: {exc}"
    except SecurityError as exc:
        return f"ERROR security: {exc}"
    except Exception as exc:  # noqa: BLE001
        return f"ERROR {name}: {exc}"
