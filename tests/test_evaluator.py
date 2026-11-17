import pytest

from promptbench import Case, evaluate, run_dataset


def test_evaluate_passes_case_insensitive_required_phrases():
    case = Case(id="welcome", input="ignored", expected_contains=("HELLO", "Sam"))
    result = evaluate(case, "Hello there, Sam!")

    assert result.passed is True
    assert result.missing_phrases == ()
    assert result.forbidden_phrases == ()


def test_evaluate_reports_missing_and_forbidden_phrases():
    case = Case(
        id="policy",
        input="input",
        expected_contains=("safe",),
        expected_not_contains=("secret",),
    )
    result = evaluate(case, "The secret is not safe.")

    assert result.passed is False
    assert result.missing_phrases == ()
    assert result.forbidden_phrases == ("secret",)


def test_case_validation_rejects_empty_id():
    with pytest.raises(ValueError, match="non-empty"):
        Case(id=" ", input="hello")


def test_evaluate_rejects_non_string_candidate():
    with pytest.raises(TypeError, match="candidate"):
        evaluate(Case(id="x", input="hello"), 12)  # type: ignore[arg-type]


def test_run_dataset_accepts_candidate_function():
    cases = [Case(id="one", input="prompt", expected_contains=("answer",))]
    results = run_dataset(cases, candidate_fn=lambda case: "The answer is 42.")

    assert len(results) == 1
    assert results[0].passed is True
