# Reproduction Trajectory — Bug 471: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/92](https://github.com/facebookresearch/detectron2/issues/92)
- **Repository:** facebookresearch/detectron2 @ `2ac32f9d5a21154484a3bb2d4ab7c94c18c08119`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Loaded the checked-out detectron2 source files directly from codebase/detectron2/data/transforms.
2. Applied compatibility shims for modern Pillow and a local fvcore stub so the transform modules could import without torch.
3. Instantiated RandomCrop('relative', (100, 100)) and called str(...) on it.
4. Observed the failure in TransformGen.__repr__ when inspect.getargspec(self.__init__) was called.

## Observed behavior

- bash run_repro.sh reached RandomCrop.__repr__ and failed with AttributeError: module 'inspect' has no attribute 'getargspec' in codebase/detectron2/data/transforms/transform_gen.py:91.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
