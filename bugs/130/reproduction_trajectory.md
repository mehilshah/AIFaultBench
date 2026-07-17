# Reproduction Trajectory — Bug 130: xformers

- **Bug report:** [https://github.com/facebookresearch/xformers/issues/1185](https://github.com/facebookresearch/xformers/issues/1185)
- **Repository:** facebookresearch/xformers @ `a2f37f8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed torch from requirements.txt.
2. Imported xformers from the local codebase path and instantiated BlockDiagonalCausalMask.from_seqlens([2, 2]).
3. Called .to(device="cpu") and observed that the returned object is BlockDiagonalMask, not BlockDiagonalCausalMask.
4. Compared materialization before and after .to(); the post-.to() mask lost the causal lower-triangular structure.

## Observed behavior

- BlockDiagonalCausalMask.from_seqlens([2, 2]) materializes a causal 4x4 block-diagonal mask.
- After calling .to(device="cpu"), the object becomes BlockDiagonalMask instead of staying BlockDiagonalCausalMask.
- The moved mask materializes as a non-causal block-diagonal mask, confirming the semantic regression.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
