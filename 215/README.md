# Bug 215 Reproduction

This bundle reproduces SDV issue 2453 from the local `codebase/`.

## What happens

The metadata validator accepts a schema where the same child foreign key
(`C.parent_id`) is used in two separate relationships:

- `A.id -> C.parent_id`
- `B.id -> C.parent_id`

The expected behavior is to reject that metadata as invalid.

## Files

- `repro.py` runs the reproduction against the local source tree.
- `requirements.txt` installs the minimal runtime dependencies used by the repro.
- `setup_env.sh` installs the Python dependencies.
- `run_repro.sh` executes the repro script.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

Expected output:

```text
VALIDATE_OK
BUG_REPRODUCED: duplicated foreign key reuse was accepted
```
