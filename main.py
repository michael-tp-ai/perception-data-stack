# def main():
#     print("Hello from perception-data-stack!")
from pathlib import Path

IGNORE = {".git", "__pycache__", ".pytest_cache", ".venv", "venv"}

def print_tree(path: Path, prefix: str = ""):
    items = sorted(
        [p for p in path.iterdir() if p.name not in IGNORE],
        key=lambda p: (p.is_file(), p.name.lower())
    )

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        print(prefix + connector + item.name)

        if item.is_dir():
            extension = "    " if is_last else "│   "
            print_tree(item, prefix + extension)

if __name__ == "__main__":
    repo_root = Path(".")
    print(repo_root.resolve().name)
    print_tree(repo_root)

if __name__ == "__main__":
    print_tree()
