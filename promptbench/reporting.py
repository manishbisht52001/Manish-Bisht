"""Output formatting helpers."""

from __future__ import annotations

import json
from collections.abc import Sequence

from .evaluator import EvaluationResult


def summarize(results: Sequence[EvaluationResult]) -> dict[str, object]:
    """Return aggregate counts and per-case outcomes."""
    passed = sum(result.passed for result in results)
    total = len(results)
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": (passed / total) if total else 0.0,
        "results": [result.to_dict() for result in results],
    }


def render_json(results: Sequence[EvaluationResult]) -> str:
    """Render a stable, indented JSON report."""
    return json.dumps(summarize(results), indent=2, ensure_ascii=False)


def render_text(results: Sequence[EvaluationResult]) -> str:
    """Render a readable terminal report."""
    summary = summarize(results)
    heading = (
        f"PromptBench: {summary['passed']}/{summary['total']} passed "
        f"({summary['pass_rate']:.0%})"
    )
    lines = [heading]
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"[{status}] {result.case_id}")
        if result.missing_phrases:
            lines.append(f"  Missing required phrases: {', '.join(result.missing_phrases)}")
        if result.forbidden_phrases:
            lines.append(f"  Found forbidden phrases: {', '.join(result.forbidden_phrases)}")
    return "\n".join(lines)
