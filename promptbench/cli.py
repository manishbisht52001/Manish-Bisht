"""Command-line interface for PromptBench."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .dataset import load_jsonl
from .evaluator import run_dataset
from .reporting import render_json, render_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="promptbench",
        description="Run deterministic checks against a JSONL prompt dataset.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run", help="evaluate a JSONL dataset")
    run_parser.add_argument("dataset", type=Path, help="path to the JSONL dataset")
    run_parser.add_argument(
        "--format", choices=("text", "json"), default="text", help="report format"
    )
    run_parser.add_argument("--output", type=Path, help="write the report to a file")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        cases = load_jsonl(args.dataset)
        results = run_dataset(cases)
        report = render_json(results) if args.format == "json" else render_text(results)
        if args.output:
            args.output.write_text(report + "\n", encoding="utf-8")
        else:
            print(report)
        return 0 if all(result.passed for result in results) else 1
    except (OSError, ValueError, TypeError) as exc:
        print(f"promptbench: error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
