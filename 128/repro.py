#!/usr/bin/env python3
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_codon() -> str:
    candidates = [
        os.environ.get("CODON_BIN"),
        shutil.which("codon"),
        str(Path.home() / ".codon" / "bin" / "codon"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return candidate
    raise FileNotFoundError("could not find the codon compiler")


def main() -> int:
    codon = find_codon()
    source = Path(__file__).with_name("repro.codon")
    output_dir = Path("repro_out")
    output_dir.mkdir(exist_ok=True)
    output = output_dir / "ndarray_pyext_repro.o"

    cmd = [
        codon,
        "build",
        "--relocation-model=pic",
        "-pyext",
        str(source),
        "-o",
        str(output),
        "-module",
        "ndarray_pyext_repro",
    ]

    print("+ " + " ".join(cmd), flush=True)
    result = subprocess.run(cmd, cwd=Path.cwd())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())

