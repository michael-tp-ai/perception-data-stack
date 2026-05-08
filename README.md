# Perception-Data-Stack

## Under Construction!


### Link to Project Overview
https://docs.google.com/document/d/17J5JO49rCufLDllJvY_zz0C7qw4GaOJGLJXC3pMLcJk/edit?tab=t.0

---

## Developer Guide

### 1. Environment Setup
We use `uv` for dependency management and `pre-commit` to ensure code quality.
```bash
# Install git hooks (do this once)
uv run pre-commit install
```

### 2. The Commit Loop (READ THIS)

Pre-commit hooks run automatically when you create a commit. They check staged files for formatting, linting, import ordering, type errors, and basic file hygiene.

The normal flow is:

1. **Check:** Ruff, Mypy, and basic file hooks inspect your staged changes.
2. **Auto-fix:** Ruff may rewrite files to fix formatting, imports, or simple lint issues.
3. **Abort:** If any hook modifies files, the commit stops. This is expected.
4. **Review:** Inspect the changes.
5. **Re-stage and commit:** Add the updated files and run the commit again.

```bash
git add .
git commit -m "your message"
````

If the commit fails because the .pre-commit auto-fixed files, review the changes, re-stage them, and commit again:

```bash
git status
git add .
git commit -m "your message"
```

---

### 3. Manual Quality Toolkit
If you want to run checks manually without committing, use these commands:

| Task | Command |
| :--- | :--- |
| **Full Suite** | `uv run pre-commit run --all-files` |
| **Lint & Fix** | `uv run ruff check --fix .` |
| **Format** | `uv run ruff format .` |
| **Type Check** | `uv run mypy .` |
| **Run Tests** | `uv run pytest` |
| **Verify Config** | `uv run python scripts/check_config.py` |

---

## System Health Check
We provide a "Doctor" script to verify your local environment is correctly configured for development. Run this after your first setup or whenever you encounter unexpected environment errors.

```bash
uv run python scripts/doctor.py
```
