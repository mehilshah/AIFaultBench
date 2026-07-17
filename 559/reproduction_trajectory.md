# Reproduction Trajectory — Bug 559: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1112](https://github.com/huggingface/accelerate/issues/1112)
- **Repository:** huggingface/accelerate @ `f054799e7fb74554591a6085ca3b920e0b10f923`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a clean virtual environment with the CPU PyTorch wheel and the local Accelerate source dependencies.
2. Loaded the local `codebase/src` copy of Accelerate.
3. Forced `PartialState` onto the distributed `MULTI_CPU` branch and stubbed `torch.distributed.all_reduce` to return the summed tensor.
4. Called the reducer with `reduction='sum'` and `reduction='mean'` on the same input tensor and observed identical outputs.

## Observed behavior

- Running `bash run_repro.sh` prints `sum=tensor([16, 20, 24, 28])` and `mean=tensor([16, 20, 24, 28])`, then raises `AssertionError: BUG: reduction='mean' returned the same tensor as reduction='sum'`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
