# Bug 323 Reproduction

This folder reproduces the `MapDataset` constructor bug from Detectron2 issue 3405.

Relevant source:
- `codebase/detectron2/data/common.py`

What the repro does:
- creates a minimal isolated environment
- imports `detectron2.data.common.MapDataset` from the local `codebase/`
- constructs `MapDataset([{"x": 1}], lambda x: x)`
- triggers `TypeError: object.__new__() takes exactly one argument (the type to instantiate)`

Run:
```bash
bash run_repro.sh
```

Expected result:
- `repro.py` fails with the `object.__new__()` `TypeError`
- output is captured in `repro_stdout.log` and `repro_stderr.log`
