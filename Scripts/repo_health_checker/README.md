# Repo Health Checker

Small CLI to check for presence of common repository files (README, LICENSE, CONTRIBUTING, etc.)
No external dependencies (Python 3.7+). Useful for maintainers and contributors.

Usage:
    python repo_health_checker.py
    python repo_health_checker.py /path/to/repo
    python repo_health_checker.py --json /path/to/repo

Add it to CI later to fail or comment on PRs when important files are missing.

