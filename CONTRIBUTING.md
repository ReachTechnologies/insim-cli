# Contributing to insim-cli

Thanks for your interest in contributing to insim-cli! This guide will help you get set up.

## Development Setup

### Prerequisites

- Python 3.10+
- An inSIM account with API access ([insim.app](https://www.insim.app))

### Install from source

```bash
git clone https://github.com/ReachTechnologies/insim-cli.git
cd insim-cli
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Run tests

```bash
pytest tests/ -v
```

### Run the CLI locally

```bash
insim --help
insim login your@email.com --key YOUR_KEY
insim contacts list --limit 5
```

## Adding a New Command

1. Create or edit the relevant module in `cli_anything/insim/core/` (e.g., `contacts.py`)
2. Add the Click command/group
3. Use `output()` from `cli_anything/insim/utils/output.py` for consistent formatting
4. Support `--json` mode for AI agent compatibility
5. Add tests in `tests/`
6. Update the command reference table in `README.md`

## Code Style

- Use type hints
- Keep functions small and focused
- Use `click` decorators for CLI arguments/options
- All API calls go through `cli_anything/insim/core/api.py`

## Pull Request Process

1. Fork the repo and create a feature branch
2. Make your changes with tests
3. Run `pytest tests/ -v` and ensure all tests pass
4. Submit a PR with a clear description of what changed and why

## Reporting Issues

Open an issue at [github.com/ReachTechnologies/insim-cli/issues](https://github.com/ReachTechnologies/insim-cli/issues) with:

- What you expected vs. what happened
- The command you ran
- Your Python version (`python --version`)
- Your OS

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
