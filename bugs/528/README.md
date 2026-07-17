# SDV issue 2725 repro bundle

This folder contains a standalone repro attempt for the reported SDV Windows
failure:

`OSError: [WinError 1114] A dynamic link library (DLL) initialization routine failed`

Reported conditions:

- SDV 1.27.0
- Python 3.10 / 3.11
- Windows
- `torch 2.9.0`
- `numpy < 2.0.0`

What this bundle does:

1. Creates a local virtual environment in `.venv`.
2. Installs the local `codebase/` in editable mode plus the bug-specific pins.
3. Runs `repro.py`, which imports `sdv` and then executes the narrow version
   test that exercises the reported collection path.

Current workspace note:

- This environment is Linux, not Windows.
- The exact `WinError 1114` DLL failure is therefore expected to be blocked
  here even if the package import path works normally.
