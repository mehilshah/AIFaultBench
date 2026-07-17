# Reproduction Trajectory — Bug 386: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3273](https://github.com/pyro-ppl/pyro/issues/3273)
- **Repository:** pyro-ppl/pyro @ `01ccf3647c1c1031b8a188488f1330b16fb5fd31`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect the CVAE example data transform in `codebase/examples/cvae/mnist.py`.
2. Inspect `MaskedBCELoss` in `codebase/examples/cvae/baseline.py`.
3. Install the isolated runtime with `bash setup_env.sh`.
4. Run `bash run_repro.sh` to trigger the BCE target validation error.

## Observed behavior

- codebase/examples/cvae/mnist.py:52-74 builds `output` tensors with `-1` in masked quadrants, so the example can feed non-binary targets downstream.
- codebase/examples/cvae/baseline.py:35-38 passes the target directly into `torch.nn.functional.binary_cross_entropy` before masking, which triggers PyTorch's target-range validation.
- Running `bash run_repro.sh` in the isolated venv prints `RuntimeError: all elements of target should be between 0 and 1` and shows `target_values` of `[-1.0, 0.0, 1.0]` in `repro_stdout.log`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
