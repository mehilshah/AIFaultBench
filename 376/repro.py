from pathlib import Path
import sys
from importlib.metadata import version as pkg_version


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from typer.testing import CliRunner

import click
import huggingface_hub
import transformers
import transformers.cli.transformers as transformers_cli
import typer


def main() -> None:
    print(f"transformers={transformers.__version__}")
    print(f"huggingface_hub={huggingface_hub.__version__}")
    print(f"typer={typer.__version__}")
    print(f"click={pkg_version('click')}")
    print("Invoking transformers CLI through Typer CliRunner...")
    runner = CliRunner()
    runner.invoke(transformers_cli.app, ["version"], catch_exceptions=False)


if __name__ == "__main__":
    main()
