# Perception-Data-Stack

### Link to Project Overview
https://docs.google.com/document/d/17J5JO49rCufLDllJvY_zz0C7qw4GaOJGLJXC3pMLcJk/edit?tab=t.0

---

# Developer Guide

This project uses a "Container-First" workflow to ensure that every developer has an identical, functional environment regardless of their host OS.

---

## Development Environment (DevContainer)

We use VS Code DevContainers + Docker to guarantee a consistent Linux environment. **You do not need to install Python or manage virtual environments on your local machine.**

### Prerequisites
1. **Docker Desktop** installed and running.
2. **VS Code** with the **Dev Containers** extension installed.

> [!TIP]
> Use [this guide](https://docs.google.com/document/d/1_OnUP8hfFFI03b7_kbIcBD_YOKiOYwMgEv-1DYLRnF4/edit?usp=sharing) if you need help with these installations.


### Quick Start
1. Clone and open this repository in VS Code.
2. Open the Command Palette (`Cmd+Shift+P`).
3. Select **`Dev Containers: Reopen in Container`**.

*Note: The first boot may take 1-3 minutes to build the image. Subsequent boots are nearly instant.*

#### How it Works
* **Invisible Environment:** `uv` installs dependencies into a secure, hidden folder (`/opt/.venv`) inside the container. This prevents OS-level collisions with your local machine.
* **Pre-configured IDE:** Ruff (linting), Mypy (typing), and Pytest are auto-installed and bound to VS Code.
* **Shared Source:** Your code and Git history are perfectly synced between your host and the container.

---
## Code Quality & Git Hooks

We use `pre-commit` to ensure all code meets our standards before it ever reaches GitHub.

### 1. The Commit Loop

Pre-commit hooks run automatically whenever you `git commit`.

1. Ruff, Mypy, and file-hygiene hooks inspect your staged changes.
2. Ruff may rewrite files to fix formatting or imports.
3. If any hook modifies a file or finds an error, the commit will stop. **This is expected behavior.**
4. Review the changes, `git add` the updated files, and commit again.

```bash
git add .
git commit -m "your message"

```
### 2. Manual Quality Toolkit
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
