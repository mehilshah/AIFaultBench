# Reproduction Trajectory — Bug 291: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/3591](https://github.com/facebookresearch/detectron2/issues/3591)
- **Repository:** facebookresearch/detectron2 @ `dfe8d368c8b7cc2be42c5c3faf9bdcc3c08257b1`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded `detectron2.structures.masks.BitMasks` from the local codebase with lightweight import stubs for unrelated optional packages.
2. Constructed `BitMasks(torch.ones(10, 256, 256))`.
3. Indexed `masks[4]` and observed the constructor assertion failure caused by the flattened `[1, 65536]` tensor.

## Observed behavior

- Running `bash run_repro.sh` reached `AssertionError: torch.Size([1, 65536])` from `codebase/detectron2/structures/masks.py:104` after `BitMasks.__getitem__` used `self.tensor[item].view(1, -1)` at line 133.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
