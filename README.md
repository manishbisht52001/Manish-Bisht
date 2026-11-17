# PromptBench

A lightweight, open-source toolkit for testing, comparing, and evaluating prompts with reproducible test cases.

> Status: early development. This repository is an initial foundation, not a claim of production readiness.

## Why PromptBench?

Prompt changes can silently alter an AI system's output. PromptBench aims to make those changes easier to reason about by letting developers:

- Keep prompt cases in version-controlled JSONL files.
- Run deterministic checks against expected text or required phrases.
- Compare outputs from different prompt versions.
- Export machine-readable results for CI pipelines.
- Add provider adapters without forcing a specific model vendor.

The first release focuses on a small, dependency-free evaluation core. Model API calls are intentionally left to adapters so the core stays easy to test and safe to run offline.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m pip install -e ".[dev]"
promptbench run examples/basic.jsonl
```

Or run directly from a checkout:

```bash
python -m promptbench.cli run examples/basic.jsonl
```

## Example dataset

Each line is a JSON object:

```json
{"id":"greeting-01","input":"Say hello to Sam.","expected_contains":["hello","Sam"]}
{"id":"summary-01","input":"Summarize: The sky is blue.","expected_contains":["sky","blue"]}
```

A dataset case may contain:

- `id` (required): unique case identifier.
- `input` (required): prompt or input text.
- `expected_contains` (optional): phrases that the result must contain.
- `expected_not_contains` (optional): phrases that must not appear.
- `tags` (optional): labels for filtering and reporting.

In this initial version, the CLI evaluates the input text as the candidate output. This makes the evaluator useful offline and gives adapter authors a stable contract to integrate with real model responses.

## Python API

```python
from promptbench import Case, evaluate

case = Case(
    id="greeting",
    input="Hello, Sam!",
    expected_contains=("hello", "sam"),
)
result = evaluate(case, candidate=case.input)
print(result.passed)
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Roadmap

- [x] JSONL dataset format
- [x] Deterministic phrase assertions
- [x] JSON and terminal reports
- [ ] Prompt template variables
- [ ] Pluggable model-provider adapters
- [ ] Baseline-versus-candidate comparisons
- [ ] CI-friendly thresholds and GitHub Action
- [ ] Documentation for community-built adapters

Roadmap items are goals, not completed features. Contributions and feedback are welcome.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before large changes. Small bug fixes, tests, docs improvements, and new examples are welcome.

## Security

Do not commit API keys, access tokens, private prompts, or confidential datasets. See [SECURITY.md](SECURITY.md) for reporting guidance.

## License

MIT. See [LICENSE](LICENSE).
