# Bug 153 Reproduction

This folder contains a self-contained repro for the tokenizer spacing regression reported in
`bug_report.txt`.

## Observed behavior

With the local `codebase/` source tree on this machine:

- `AutoTokenizer.from_pretrained("mlx-community/Llama-3.2-1B-Instruct-4bit").decode([128000, 64, 1174, 65])`
- returns `"<|begin_of_text|>a ,b"`

The bug report expected the v4 behavior:

- `"<|begin_of_text|>a,b"`

## Files

- `repro.py`: minimal Python repro
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates `.venv` and installs dependencies
- `run_repro.sh`: runs the repro and captures logs
- `reproduction.json`: machine-readable result summary
- `repro_stdout.log` / `repro_stderr.log`: captured output from the verified run

## Reproduction

```bash
bash run_repro.sh
```

The script exits with status `1` when the mismatch is observed.
