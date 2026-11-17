import json

from promptbench.cli import main


def test_cli_evaluates_saved_outputs(tmp_path, capsys):
    dataset = tmp_path / "cases.jsonl"
    outputs = tmp_path / "outputs.jsonl"
    dataset.write_text(
        json.dumps(
            {"id": "welcome", "input": "Write a greeting", "expected_contains": ["hello"]}
        )
        + "\n",
        encoding="utf-8",
    )
    outputs.write_text(
        json.dumps({"case_id": "welcome", "output": "Hello, Sam!"}) + "\n",
        encoding="utf-8",
    )
    assert main(["run", str(dataset), "--outputs", str(outputs)]) == 0
    assert "[PASS] welcome" in capsys.readouterr().out


def test_cli_fails_when_saved_output_is_missing(tmp_path, capsys):
    dataset = tmp_path / "cases.jsonl"
    outputs = tmp_path / "outputs.jsonl"
    dataset.write_text('{"id":"welcome","input":"Write a greeting"}\n', encoding="utf-8")
    outputs.write_text("", encoding="utf-8")
    assert main(["run", str(dataset), "--outputs", str(outputs)]) == 2
    assert "missing outputs for: welcome" in capsys.readouterr().err


def test_cli_fails_when_output_has_unknown_case_id(tmp_path, capsys):
    dataset = tmp_path / "cases.jsonl"
    outputs = tmp_path / "outputs.jsonl"
    dataset.write_text('{"id":"welcome","input":"Write a greeting"}\n', encoding="utf-8")
    outputs.write_text('{"case_id":"other","output":"Hello"}\n', encoding="utf-8")
    assert main(["run", str(dataset), "--outputs", str(outputs)]) == 2
    assert "unknown case IDs: other" in capsys.readouterr().err
