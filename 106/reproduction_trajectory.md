# Reproduction Trajectory — Bug 106: timm

- **Bug report:** [https://github.com/huggingface/pytorch-image-models/issues/2282](https://github.com/huggingface/pytorch-image-models/issues/2282)
- **Repository:** huggingface/pytorch-image-models @ `6ab2af610db6cfafa505589419894c2dd34d59fc`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtualenv and installed torch 2.4.1 CPU wheels.
2. Imported timm.layers.Mlp from the local codebase.
3. Ran the same input tensor through Mlp as batch size 1 and batch size 2.
4. Observed that the two batch-2 rows are equal, but batch-1 vs batch-2 row 0 is not equal.

## Observed behavior

- On this machine, the repro fails the final equality assertion even on CPU. The identical-sample outputs within batch size 2 match each other, but batch size 1 vs batch size 2 differ with max abs diff 0.000244140625.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
