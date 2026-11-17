import json

import pytest

from promptbench import load_jsonl, load_outputs_jsonl


def test_load_jsonl_reads_cases_and_skips_blank_lines(tmp_path):
    path = tmp_path / "cases.jsonl"
    path.write_text(
        "\n"
        + json.dumps({"id": "a", "input": "Hello", "tags": ["smoke"]})
        + "\n",
        encoding="utf-8",
    )
    cases = load_jsonl(path)
    assert len(cases) == 1
    assert cases[0].id == "a"
    assert cases[0].tags == ("smoke",)


def test_load_jsonl_reports_invalid_json_line(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"id": "a",\n', encoding="utf-8")
    with pytest.raises(ValueError, match="line 1: invalid JSON"):
        load_jsonl(path)


def test_load_jsonl_rejects_duplicate_ids(tmp_path):
    path = tmp_path / "duplicate.jsonl"
    path.write_text(
        '{"id":"same","input":"one"}\n{"id":"same","input":"two"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate"):
        load_jsonl(path)


def test_load_jsonl_rejects_non_array_assertions(tmp_path):
    path = tmp_path / "wrong-type.jsonl"
    path.write_text(
        '{"id":"a","input":"hello","expected_contains":"hello"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="array of strings"):
        load_jsonl(path)


def test_load_outputs_jsonl_maps_case_ids_to_outputs(tmp_path):
    path = tmp_path / "outputs.jsonl"
    path.write_text(
        '{"case_id":"welcome","output":"Hello, Sam!"}\n'
        '{"case_id":"summary","output":"A short summary."}\n',
        encoding="utf-8",
    )
    assert load_outputs_jsonl(path) == {
        "welcome": "Hello, Sam!",
        "summary": "A short summary.",
    }


def test_load_outputs_jsonl_rejects_duplicate_case_ids(tmp_path):
    path = tmp_path / "duplicate-outputs.jsonl"
    path.write_text(
        '{"case_id":"a","output":"one"}\n{"case_id":"a","output":"two"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate case_id"):
        load_outputs_jsonl(path)


def test_load_outputs_jsonl_requires_string_output(tmp_path):
    path = tmp_path / "bad-output.jsonl"
    path.write_text('{"case_id":"a","output":42}\n', encoding="utf-8")
    with pytest.raises(TypeError, match="'output' must be a string"):
        load_outputs_jsonl(path)
