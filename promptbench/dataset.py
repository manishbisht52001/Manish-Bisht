"""Load PromptBench JSONL datasets."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evaluator import Case


def _string_tuple(value: Any, field_name: str, line_number: int) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"line {line_number}: {field_name} must be a JSON array of strings")
    return tuple(value)


def load_jsonl(path: str | Path) -> list[Case]:
    """Read cases from a UTF-8 JSON Lines file with helpful line-level errors."""
    dataset_path = Path(path)
    cases: list[Case] = []
    seen_ids: set[str] = set()

    try:
        content = dataset_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(f"could not read dataset {dataset_path}: {exc}") from exc

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        try:
            item = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"line {line_number}: invalid JSON at column {exc.colno}: {exc.msg}"
            ) from exc
        if not isinstance(item, dict):
            raise TypeError(f"line {line_number}: each dataset line must be a JSON object")

        case_id = item.get("id")
        case_input = item.get("input")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"line {line_number}: 'id' must be a non-empty string")
        if case_id in seen_ids:
            raise ValueError(f"line {line_number}: duplicate case id {case_id!r}")
        if not isinstance(case_input, str):
            raise TypeError(f"line {line_number}: 'input' must be a string")

        try:
            case = Case(
                id=case_id,
                input=case_input,
                expected_contains=_string_tuple(
                    item.get("expected_contains"), "expected_contains", line_number
                ),
                expected_not_contains=_string_tuple(
                    item.get("expected_not_contains"), "expected_not_contains", line_number
                ),
                tags=_string_tuple(item.get("tags"), "tags", line_number),
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
        seen_ids.add(case_id)
        cases.append(case)

    return cases
