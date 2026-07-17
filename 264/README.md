# Bug 264 Reproduction

This folder reproduces the tinygrad bug reported at:
`https://github.com/tinygrad/tinygrad/issues/13853`

## What fails

The local `codebase/` currently produces the wrong shard after realizing a sharded tensor and then shrinking it:

- expected: `[2, 3]`
- observed: `[0, 1]`

The second case in the report also fails:

- expected: `[0, 1]`
- observed: `[0, 0]`

## How to run

```bash
bash setup_env.sh
bash run_repro.sh
```

The reproduction command writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Files

- `repro.py` - minimal script from the issue report
- `requirements.txt` - minimal dependency list
- `setup_env.sh` - installs the Python dependencies
- `run_repro.sh` - runs the repro and captures logs
- `reproduction.json` - machine-readable result
