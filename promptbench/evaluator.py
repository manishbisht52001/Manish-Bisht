"""Deterministic evaluation primitives for prompt outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True, slots=True)
class Case:
    """A single evaluation example using deterministic phrase assertions."""

    id: str
    input: str
    expected_contains: tuple[str, ...] = ()
    expected_not_contains: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("case id must be a non-empty string")
        if not isinstance(self.input, str):
            raise TypeError("case input must be a string")
        for field_name in ("expected_contains", "expected_not_contains", "tags"):
            value = getattr(self, field_name)
            if not isinstance(value, tuple) or any(not isinstance(item, str) for item in value):
                raise TypeError(f"{field_name} must be a tuple of strings")
        if any(not phrase for phrase in self.expected_contains + self.expected_not_contains):
            raise ValueError("expected phrases must not be empty")


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    """Outcome of evaluating one candidate output against a case."""

    case_id: str
    passed: bool
    candidate: str
    missing_phrases: tuple[str, ...] = ()
    forbidden_phrases: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""
        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "candidate": self.candidate,
            "missing_phrases": list(self.missing_phrases),
            "forbidden_phrases": list(self.forbidden_phrases),
            "tags": list(self.tags),
        }


def evaluate(case: Case, candidate: str) -> EvaluationResult:
    """Evaluate candidate using the deterministic assertions defined by case."""
    if not isinstance(case, Case):
        raise TypeError("case must be a Case instance")
    if not isinstance(candidate, str):
        raise TypeError("candidate must be a string")

    normalized = candidate.casefold()
    missing = tuple(
        phrase for phrase in case.expected_contains if phrase.casefold() not in normalized
    )
    forbidden = tuple(
        phrase for phrase in case.expected_not_contains if phrase.casefold() in normalized
    )
    return EvaluationResult(
        case_id=case.id,
        passed=not missing and not forbidden,
        candidate=candidate,
        missing_phrases=missing,
        forbidden_phrases=forbidden,
        tags=case.tags,
    )


def run_dataset(
    cases: Iterable[Case],
    candidate_fn: Callable[[Case], str] | None = None,
) -> list[EvaluationResult]:
    """Run cases using a candidate function.

    The candidate function receives a Case and must return generated text. When omitted,
    the case input is evaluated directly, which is useful for offline examples.
    """
    results: list[EvaluationResult] = []
    for case in cases:
        candidate = case.input if candidate_fn is None else candidate_fn(case)
        results.append(evaluate(case, candidate))
    return results
