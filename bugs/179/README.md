# Reproduction Bundle

This folder reproduces the Lark issue described in `bug_report.txt`.

## What fails

An embedded `Transformer` on an LALR parser rejects a terminal callback that returns a Python value:

```python
class T(Transformer):
    NUM = int

Lark(grammar, parser="lalr", transformer=T()).parse("32")
```

The runtime error is:

`lark.exceptions.LexError: Callbacks must return a token (returned 32)`

## How to run

1. Bootstrap the environment:

   ```bash
   ./setup_env.sh
   ```

2. Run the repro:

   ```bash
   ./run_repro.sh
   ```

## Files

- `repro.py`: minimal failing snippet
- `requirements.txt`: installs the local `codebase/` package in editable mode
- `setup_env.sh`: creates a local virtual environment and installs dependencies
- `run_repro.sh`: executes the repro inside the virtual environment
- `manifest.json`: compact metadata for the bundle
