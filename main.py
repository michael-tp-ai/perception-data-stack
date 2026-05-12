# """Temp file for testing on the go - will remove for actual production."""

# from pathlib import Path


# IGNORE_DIRS = {
#     ".git",
#     "__pycache__",
#     ".pytest_cache",
#     ".ruff_cache",
#     ".mypy_cache",
#     ".venv",
#     "venv",
#     "env",
#     ".env",
#     "node_modules",
#     "dist",
#     "build",
# }

# IGNORE_FILES = {
#     ".DS_Store",
# }

# IGNORE_SUFFIXES = {
#     ".pyc",
#     ".pyo",
#     ".data.json",
#     ".meta.json",
# }


# def should_ignore(path: Path) -> bool:
#     if path.is_dir() and path.name in IGNORE_DIRS:
#         return True

#     if path.is_file() and path.name in IGNORE_FILES:
#         return True

#     if any(path.name.endswith(suffix) for suffix in IGNORE_SUFFIXES):
#         return True

#     return False


# def print_tree(path: Path, prefix: str = ""):
#     items = sorted(
#         [p for p in path.iterdir() if not should_ignore(p)],
#         key=lambda p: (p.is_file(), p.name.lower()),
#     )

#     for index, item in enumerate(items):
#         is_last = index == len(items) - 1
#         connector = "└── " if is_last else "├── "
#         print(prefix + connector + item.name)

#         if item.is_dir():
#             extension = "    " if is_last else "│   "
#             print_tree(item, prefix + extension)


# def main():
#     repo_root = Path(".").resolve()
#     print(repo_root.name)
#     print_tree(repo_root)


# if __name__ == "__main__":
#     main()
