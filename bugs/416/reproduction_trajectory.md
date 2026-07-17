# Reproduction Trajectory — Bug 416: pyro-ppl

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3218](https://github.com/pyro-ppl/pyro/issues/3218)
- **Repository:** pyro-ppl/pyro @ `b8e0c3ce78b420c7484d3761791f832b988b3a02`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a CUDA-enabled isolated venv and installed torch 2.11.0+cu128 with the checked-out Pyro snapshot b8e0c3ce.
2. Ran the baseline path `torch.as_tensor(y.cuda())` without a default device and observed the correct 3-element CUDA tensor.
3. Set the default device to CUDA and ran `torch.as_tensor(y)` on ProvenanceTensor, which returned an empty CUDA tensor and triggered the assertion.

## Observed behavior

- baseline_result preserved the original data: tensor([1., 2., 3.], device='cuda:0') with shape (3,)
- bug_result under torch.set_default_device('cuda') became tensor([], device='cuda:0') with shape (0,)
- repro.py ended with AssertionError: expected shape (3,), got (0,)

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh > repro_stdout.log 2> repro_stderr.log
```
