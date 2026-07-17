# Bug 459 Reproduction

This folder reproduces NumPyro issue 2064 on commit `ddbd0b876d3cf07d457683d520f00c85f0cc0bb8`.

## What fails

`numpyro.infer.inspect.get_model_relations()` raises a JAX `TypeError` when a `param` site is initialized with a lambda function.

## Run

```bash
bash run_repro.sh
```

The run script writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Notes

- The bundle uses a local editable checkout at `codebase/`.
- The pinned dependency set was chosen to keep this old NumPyro commit runnable on Python 3.12.
