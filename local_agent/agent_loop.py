"""Tool-calling agent loop (Ollama). Inspired by ollama-python examples and local-cli."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import ollama_client
from .config import MAX_TOOL_ROUNDS, OLLAMA_MODEL, ROOT
from .prompts import build_system_prompt, default_user_goal
from .tools_registry import SCHEMAS, dispatch


def _message_to_dict(msg: Any) -> dict[str, Any]:
    if isinstance(msg, dict):
        return msg
    # ollama may return objects; we use raw JSON dicts from API
    return dict(msg)


def _extract_tool_calls(message: dict[str, Any]) -> list[dict[str, Any]]:
    calls = message.get("tool_calls") or []
    return list(calls)


def _tool_args(call: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    fn = call.get("function") or {}
    name = fn.get("name") or call.get("name") or ""
    raw = fn.get("arguments", {})
    if isinstance(raw, str):
        try:
            args = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            args = {}
    elif isinstance(raw, dict):
        args = raw
    else:
        args = {}
    return name, args


def run_agent(
    project_id: str,
    user_message: str | None = None,
    model: str | None = None,
    max_rounds: int | None = None,
    verbose: bool = True,
) -> str:
    model = model or OLLAMA_MODEL
    max_rounds = max_rounds or MAX_TOOL_ROUNDS
    goal = user_message or default_user_goal(project_id)

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": build_system_prompt(project_id)},
        {"role": "user", "content": goal},
    ]

    session_dir = ROOT / "projects" / project_id / "state" / "local_sessions"
    session_dir.mkdir(parents=True, exist_ok=True)
    session_path = session_dir / f"session_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.jsonl"

    final_text = ""
    for round_i in range(1, max_rounds + 1):
        if verbose:
            print(f"\n--- round {round_i}/{max_rounds} ({model}) ---")
        resp = ollama_client.chat(messages=messages, tools=SCHEMAS, model=model)
        message = _message_to_dict(resp.get("message") or {})
        messages.append(message)

        with session_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"round": round_i, "message": message}, ensure_ascii=False) + "\n")

        content = (message.get("content") or "").strip()
        if content and verbose:
            # qwen3 may include thinking; print truncated
            preview = content if len(content) < 1200 else content[:1200] + "..."
            print(preview)

        tool_calls = _extract_tool_calls(message)
        if not tool_calls:
            final_text = content
            break

        for call in tool_calls:
            name, args = _tool_args(call)
            if verbose:
                print(f"[tool] {name}({args})")
            result = dispatch(name, args)
            if verbose:
                rprev = result if len(result) < 500 else result[:500] + "..."
                print(f"[result] {rprev}")
            tool_msg = {
                "role": "tool",
                "content": result,
                "tool_name": name,
            }
            messages.append(tool_msg)
            with session_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"tool": name, "args": args, "result_preview": result[:2000]}, ensure_ascii=False) + "\n")
    else:
        final_text = final_text or "(stopped: max tool rounds reached — state should be on disk)"

    if verbose:
        print(f"\nSession log: {session_path.relative_to(ROOT)}")
    return final_text
