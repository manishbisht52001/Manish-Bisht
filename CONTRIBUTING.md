# Contributing

Thanks for considering a contribution.

## Before opening a pull request

1. Search existing issues and pull requests to avoid duplicate work.
2. For a substantial change, open an issue describing the problem and proposed solution.
3. Keep changes focused and include tests for new behavior or bug fixes.

## Local setup

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Pull request checklist

- [ ] The change has a clear purpose.
- [ ] Tests cover the changed behavior.
- [ ] Documentation or examples are updated where needed.
- [ ] No secrets, private datasets, or unrelated generated files are included.
- [ ] The full test suite and lint checks pass.

Please be respectful and constructive in discussions. Small documentation fixes are welcome.
