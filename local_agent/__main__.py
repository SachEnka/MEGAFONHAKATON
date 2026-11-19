"""CLI: python -m local_agent --project demo-megakino"""
from __future__ import annotations

import argparse
import sys

from . import ollama_client
from .agent_loop import run_agent
from .config import OLLAMA_HOST, OLLAMA_MODEL, ROOT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Local Strategist agent (Ollama). Data and inference stay on this machine."
    )
    parser.add_argument("--project", default="demo-megakino", help="projects/<id>")
    parser.add_argument("--model", default=None, help=f"Ollama model (default: {OLLAMA_MODEL})")
    parser.add_argument("--message", default=None, help="Override user goal message")
    parser.add_argument(
        "--phase",
        default=None,
        help="Hint phase for resume message (intake|gather|research|options|strategy|after)",
    )
    parser.add_argument("--persona", default=None, help="Load .cursor/rules/<slug>.mdc as extra system context")
    parser.add_argument("--max-rounds", type=int, default=None)
    parser.add_argument("--check", action="store_true", help="Only check Ollama health and exit")
    parser.add_argument("-q", "--quiet", action="store_true")
    args = parser.parse_args(argv)

    health = ollama_client.check_health()
    if not health.get("ok"):
        print("Ollama is not reachable at", OLLAMA_HOST, file=sys.stderr)
        print(health.get("error"), file=sys.stderr)
        print("Start with: ollama serve", file=sys.stderr)
        return 2

    models = health.get("models") or []
    model = args.model or OLLAMA_MODEL
    if args.check:
        print("Ollama OK", OLLAMA_HOST)
        print("Models:", ", ".join(models) or "(none)")
        print("Default model:", model)
        print("Repo:", ROOT)
        if model not in models and not any(m.startswith(model.split(":")[0]) for m in models):
            print(f"WARN: `{model}` not in ollama list. Pull: ollama pull {model}", file=sys.stderr)
            return 1
        return 0

    if model not in models and not any(str(m).startswith(model) for m in models):
        # allow tags like qwen3:8b when list has exact match only
        exact = model in models
        if not exact:
            print(
                f"Model `{model}` not found. Available: {models}\n"
                f"Pull one with tool calling, e.g.: ollama pull qwen3:8b",
                file=sys.stderr,
            )
            return 1

    project_dir = ROOT / "projects" / args.project
    if not project_dir.exists():
        print(f"Project not found: {project_dir}", file=sys.stderr)
        return 1

    print(f"Local Strategist | model={model} | project={args.project} | host={OLLAMA_HOST}")
    print("Security: path sandbox=repo, web=allowlist+SSRF guard, no cloud API keys required.")

    user_message = args.message
    if user_message is None and args.phase:
        user_message = (
            f"Resume project `{args.project}`. Focus on phase `{args.phase}` only. "
            f"Read state/CURRENT.md and the matching skill under skills/. "
            f"Write artifacts to disk; ask_user only on human gate."
        )
    if args.persona:
        persona_path = ROOT / ".cursor" / "rules" / f"{args.persona}.mdc"
        if not persona_path.exists():
            # allow filename without assuming .mdc already
            alt = ROOT / ".cursor" / "rules" / args.persona
            persona_path = alt if alt.exists() else persona_path
        if persona_path.exists():
            extra = persona_path.read_text(encoding="utf-8")[:12000]
            user_message = (user_message or "") + f"\n\n# Persona rule ({persona_path.name})\n{extra}"
        else:
            print(f"WARN: persona not found: {args.persona}", file=sys.stderr)

    text = run_agent(
        project_id=args.project,
        user_message=user_message,
        model=model,
        max_rounds=args.max_rounds,
        verbose=not args.quiet,
    )
    print("\n=== FINAL ===")
    print(text or "(empty)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
