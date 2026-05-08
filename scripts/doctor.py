import importlib
import subprocess
import sys
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize Rich console
console = Console()

# ---------------------------------------------------------
# Check Functions
# ---------------------------------------------------------


def check_python() -> tuple[bool, str]:
    """Check if Python version meets the >=3.10 requirement."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major == 3 and version.minor >= 10:
        return True, f"Python {version_str} (Valid)"
    return False, f"Python {version_str} (Requires >= 3.10)"


def check_uv_sync() -> tuple[bool, str]:
    """Check if the uv lockfile exists and the environment is active."""
    root_dir = Path(__file__).resolve().parent.parent

    if not (root_dir / "uv.lock").exists():
        return False, "uv.lock not found. Run 'uv sync'."

    try:
        # Check if uv is installed and accessible
        subprocess.run(["uv", "--version"], check=True, capture_output=True, text=True)
        return True, "uv lockfile exists and uv is installed"
    except FileNotFoundError:
        return False, "'uv' command not found in PATH."
    except subprocess.CalledProcessError:
        return False, "'uv' command failed."


def check_directories() -> tuple[bool, str]:
    """Ensure required output directories exist and are writable."""
    # The artifacts direcotry is not tracked ~ is in .gitignore -
    #  which is why we check for it here

    root_dir = Path(__file__).resolve().parent.parent
    artifacts_dir = root_dir / "artifacts"

    try:
        # Create it if it doesn't exist
        artifacts_dir.mkdir(parents=True, exist_ok=True)

        # Test write permissions
        test_file = artifacts_dir / ".write_test"
        test_file.touch()
        test_file.unlink()  # Clean up
        return True, "artifacts/ is writable"
    except PermissionError:
        return False, "artifacts/ is NOT writable (Permission Denied)"
    except Exception as e:
        return False, f"Failed to verify artifacts/: {e}"


def check_imports() -> tuple[bool, str]:
    """Verify that core third-party dependencies are installed."""
    core_libs = ["pydantic", "hydra", "loguru", "rich", "omegaconf"]
    missing = []

    for lib in core_libs:
        try:
            importlib.import_module(lib)
        except ImportError:
            missing.append(lib)

    if missing:
        return False, f"Missing packages: {', '.join(missing)}"
    return True, "All core libraries imported successfully"


def check_config() -> tuple[bool, str]:
    """Verify that the base Hydra config compiles against Pydantic models."""
    try:
        from hydra import compose, initialize_config_dir

        from perception_stack.config.config_loader import load_and_validate_config

        config_dir = Path(__file__).resolve().parent.parent / "configs"

        with initialize_config_dir(version_base="1.3", config_dir=str(config_dir)):
            raw_cfg = compose(config_name="config")
            # This triggers Pydantic's strict validation
            load_and_validate_config(raw_cfg)

        return True, "Base config is structurally valid"
    except Exception as e:
        return False, f"Config validation failed: {e!s}"


# ---------------------------------------------------------
# Main Execution
# ---------------------------------------------------------


def main() -> None:
    console.print(
        Panel("[bold cyan]Perception Stack: Factory Floor Health Check[/bold cyan]", expand=False)
    )
    logger.info("Starting system diagnostics...")

    # Define the checks
    checks = {
        "Python Version": check_python,
        "UV Environment": check_uv_sync,
        "Directory Access": check_directories,
        "Core Imports": check_imports,
        "Base Config Check": check_config,
    }

    # Prepare the Rich Table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="dim", width=20)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Message")

    all_passed = True

    # Run each check and populate the table
    for name, func in checks.items():
        logger.debug(f"Running check: {name}...")
        passed, message = func()

        if passed:
            status_icon = "[green]✔ PASS[/green]"
        else:
            status_icon = "[red]✖ FAIL[/red]"
            all_passed = False
            logger.error(f"{name} failed: {message}")

        table.add_row(name, status_icon, message)

    console.print("\n")
    console.print(table)
    console.print("\n")

    # Final Verdict
    if all_passed:
        logger.success("Diagnostics complete - this environment is 100% healthy.")
        console.print("[bold green]✅ Ready to build! [/bold green]")
        sys.exit(0)
    else:
        logger.critical("Diagnostics failed. Please fix the errors above before proceeding.")
        console.print("[bold red]🛑 Environment is unhealthy. Check the logs above.[/bold red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
