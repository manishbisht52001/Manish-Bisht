# PromptBench

[![CI](https://github.com/manishbisht52001/Manish-Bisht/actions/workflows/ci.yml/badge.svg)](https://github.com/manishbisht52001/Manish-Bisht/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

A small, provider-neutral toolkit for keeping prompt checks in version control and evaluating text outputs with repeatable assertions.

> **Project status:** early development (0.1.0). The current release provides a deterministic evaluation core. It does not call an LLM provider or perform semantic grading.

## Why PromptBench?

Prompt changes can silently alter an AI system's output. PromptBench provides a minimal foundation for writing repeatable checks around those changes:

- Store test cases as readable JSONL files.
- Check required and forbidden phrases without calling an external API.
- Produce terminal or JSON reports that can be consumed by CI.
- Use the Python API to connect your own model or prompt runner.
- Keep the core dependency-free and provider-neutral.

The project intentionally starts with deterministic checks. Exact phrase assertions are not a substitute for human review or semantic evaluation; they are a fast, predictable first layer.

## Quick start

Requires Python 3.10 or newer.

```bash
git clone https://github.com/manishbisht52001/Manish-Bisht.git
cd Manish-Bisht
python -m pip install -e ".[dev]"
promptbench run examples/basic.jsonl
```

To write a JSON report:

```bash
promptbench run examples/basic.jsonl --format json --output report.json
```

The command exits with code 0 when every case passes, 1 when one or more cases fail, and 2 when the dataset cannot be loaded or validated.

## Dataset format

PromptBench reads UTF-8 JSON Lines files: one JSON object per non-empty line.

```json
{"id":"greeting-01","input":"Hello, Sam! Welcome to PromptBench.","expected_contains":["hello","sam"],"expected_not_contains":["goodbye"],"tags":["greeting","smoke"]}
{"id":"summary-01","input":"The sky is blue and the grass is green.","expected_contains":["sky","blue"],"tags":["basic"]}
```

| Field | Required | Description |
|---|---|---|
| `id` | Yes | Unique, non-empty case identifier |
| `input` | Yes | Input or prompt text |
| `expected_contains` | No | Phrases that must appear in the candidate output |
| `expected_not_contains` | No | Phrases that must not appear |
| `tags` | No | String labels for organizing cases |

Phrase checks are case-insensitive substring matches. Duplicate IDs, malformed JSON, and incorrectly typed fields produce line-numbered errors. Blank lines and lines beginning with `#` are ignored.

### Important: current CLI behavior

The initial CLI evaluates each case's `input` as its candidate output. This makes the sample dataset runnable offline and tests the evaluator itself. To evaluate real model outputs, call the Python API with a candidate function or integrate your own provider adapter. The CLI does not yet call a model.

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
2. **Provider-neutral:** users supply candidate outputs through a small Python function.
3. **Inspectable:** datasets and JSON reports are plain text.
4. **Small surface area:** the runtime package has no third-party dependencies.
5. **Honest evaluation:** deterministic phrase checks are clearly distinguished from semantic quality judgments.

## Roadmap

- [x] JSONL dataset format and validation
- [x] Required and forbidden phrase assertions
- [x] Python API and candidate function hook
- [x] Terminal and JSON reports
- [x] GitHub Actions CI
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
