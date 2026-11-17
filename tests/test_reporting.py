from promptbench import Case, evaluate
from promptbench.reporting import render_json, render_text, summarize


def test_summarize_empty_results():
    summary = summarize([])

    assert summary["total"] == 0
    assert summary["pass_rate"] == 0.0


def test_reports_include_case_status():
    case = Case(id="hello", input="hello", expected_contains=("hello",))
    result = evaluate(case, "hello")

    assert '"passed": true' in render_json([result])
    assert "[PASS] hello" in render_text([result])
