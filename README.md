# PromptBench

[![CI](https://github.com/manishbisht52001/PromptBench/actions/workflows/ci.yml/badge.svg)](https://github.com/manishbisht52001/PromptBench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

A lightweight, provider-neutral toolkit for testing prompts and evaluating model outputs with repeatable, version-controlled checks.

> **Project status:** early development (0.1.0). PromptBench provides deterministic phrase-based evaluation. It does not make model API calls or perform semantic grading.

## Why PromptBench?

Prompt changes can silently alter an AI system's output. PromptBench provides a minimal foundation for repeatable checks:

- Store test cases as readable JSONL files.
- Evaluate saved outputs from any model or provider.
- Check required and forbidden phrases without external API calls.
- Produce terminal or JSON reports for local workflows and CI.
- Connect your own model or prompt runner through the Python API.
- Keep the runtime core dependency-free and provider-neutral.

Exact phrase assertions are not a substitute for human review or semantic evaluation; they are a fast, predictable first layer.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/manishbisht52001/PromptBench.git
cd PromptBench
python -m pip install -e ".[dev]"
promptbench run examples/basic.jsonl
```

The sample command runs the evaluator against the dataset's input text, making the project runnable offline.

## Evaluate saved model outputs

Export one output per dataset case as JSONL, matching by case ID:

```json
{"case_id":"greeting-01","output":"Hello, Sam! Welcome to PromptBench."}
{"case_id":"summary-01","output":"The sky is blue and the grass is green."}
```

Then run:

```bash
promptbench run examples/basic.jsonl --outputs model-outputs.jsonl
```

Every dataset case must have exactly one matching output. Missing outputs, unknown case IDs, and duplicate IDs are reported as errors. Add `--format json` for machine-readable results. PromptBench evaluates outputs generated elsewhere; it does not call a model provider.

To write a JSON report:

```bash
promptbench run examples/basic.jsonl --outputs model-outputs.jsonl --format json --output report.json
```

The command exits with code 0 when every case passes, 1 when one or more cases fail, and 2 when the dataset cannot be loaded or validated.

## Dataset format

PromptBench reads UTF-8 JSON Lines files: one JSON object per non-empty line.

```json
{"id":"greeting-01","input":"Write a friendly greeting for Sam.","expected_contains":["hello","sam"],"expected_not_contains":["goodbye"],"tags":["greeting","smoke"]}
{"id":"summary-01","input":"Summarize the main point.","expected_contains":["sky","blue"],"tags":["basic"]}
```

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Unique, non-empty case identifier |
| `input` | Yes | Input or prompt text |
| `expected_contains` | No | Phrases that must appear in the candidate output |
| `expected_not_contains` | No | Phrases that must not appear |
| `tags` | No | String labels for organizing cases |

Phrase checks are case-insensitive substring matches. Duplicate IDs, malformed JSON, and incorrectly typed fields produce line-numbered errors. Blank lines and lines beginning with `#` are ignored.

## Python API

```python
from promptbench import Case, evaluate, load_jsonl, run_dataset

case = Case(
    id="greeting",
    input="Write a friendly greeting for Sam.",
    expected_contains=("hello", "sam"),
    expected_not_contains=("goodbye",),
)

# Replace this function with your own model/provider call.
def generate(case: Case) -> str:
    return "Hello, Sam! Welcome."

result = evaluate(case, candidate=generate(case))
print(result.passed)

# Or run a whole version-controlled dataset.
cases = load_jsonl("examples/basic.jsonl")
results = run_dataset(cases, candidate_fn=generate)
```

The candidate function receives a `Case` and must return a string. Provider credentials and network calls stay in your integration code, not in PromptBench's core.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

Every push and pull request runs the test suite and Ruff lint checks through GitHub Actions.

## Design principles

1. **Reproducible:** the core evaluator does not use model calls, randomness, or network access.
2. **Provider-neutral:** users supply candidate outputs through a small Python function or saved-output file.
3. **Inspectable:** datasets and JSON reports are plain text.
4. **Small surface area:** the runtime package has no third-party dependencies.
5. **Honest evaluation:** deterministic phrase checks are clearly distinguished from semantic quality judgments.

## Roadmap

- [x] JSONL dataset format and validation
- [x] Required and forbidden phrase assertions
- [x] Python API and candidate function hook
- [x] Terminal and JSON reports
- [x] GitHub Actions CI
- [x] CLI evaluation of saved model outputs
- [ ] Prompt template variables
- [ ] Baseline-versus-candidate comparison reports
- [ ] Provider adapter examples
- [ ] Optional semantic graders with clearly documented limitations
- [ ] CI thresholds and GitHub Action

Roadmap items are goals, not completed features. Please check open issues before starting a large change.

## Contributing

Bug reports, documentation improvements, test cases, and focused feature proposals are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Please do not submit generated activity or low-quality bulk changes; thoughtful, reviewed contributions matter more than volume.

## Security

Never commit API keys, access tokens, private prompts, or confidential datasets. See [SECURITY.md](SECURITY.md) for reporting guidance.

## License

PromptBench is released under the MIT License. See [LICENSE](LICENSE).
