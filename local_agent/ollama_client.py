"""Minimal Ollama chat client (stdlib). Pattern: ollama-python tool loop / local-cli."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from .config import OLLAMA_HOST, OLLAMA_MODEL, REQUEST_TIMEOUT


class OllamaError(Exception):
    pass


def check_health(host: str = OLLAMA_HOST) -> dict[str, Any]:
    url = f"{host}/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        names = [m.get("name") for m in data.get("models", [])]
        return {"ok": True, "models": names}
    except Exception as exc:  # noqa: BLE001 — surface as health payload
        return {"ok": False, "error": str(exc)}


def chat(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    model: str = OLLAMA_MODEL,
    host: str = OLLAMA_HOST,
    temperature: float = 0.2,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if tools:
        payload["tools"] = tools

    req = urllib.request.Request(
        f"{host}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise OllamaError(f"Ollama HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise OllamaError(
            f"Cannot reach Ollama at {host}. Start it with `ollama serve`. ({exc})"
        ) from exc
