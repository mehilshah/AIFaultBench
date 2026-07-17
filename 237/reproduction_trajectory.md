# Reproduction Trajectory — Bug 237: jaxtyping

- **Bug report:** [https://github.com/patrick-kidger/jaxtyping/issues/249](https://github.com/patrick-kidger/jaxtyping/issues/249)
- **Repository:** patrick-kidger/jaxtyping @ `f4ca4c9`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh virtualenv and install `numpy`, `torch==2.13.0+cpu`, and `typeguard==2.13.3`.
2. Install the local `codebase/` as an editable package so `jaxtyping` metadata is available.
3. Run `bash run_repro.sh` to call a mismatched `jaxtyped` matmul and capture the resulting `TypeCheckError`.

## Observed behavior

- Running `bash run_repro.sh` prints `reproducible=True` and `verbose_tensor_repr=True`; the captured TypeCheckError includes `Actual value: tensor([[...` for the bad `y` argument instead of a compact shape/dtype summary.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
cd ../237 && bash run_repro.sh
```
