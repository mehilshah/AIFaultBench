# Bug 489

This folder contains the reproducible bundle for the timm `lsnet_t` report.

What is here:
- `bug_report.txt`
- `codebase/`
- Reproduction artifacts

How to run:
- `bash run_repro.sh`

Observed outcome:
- `timm.create_model("lsnet_t")` fails before the custom package is imported.
- After importing a package that registers `lsnet_t`, model creation succeeds.
- That means the reported failure is not a core `timm` loader regression in this codebase; it is a model-registration problem.

Relevant source paths:
- [`codebase/timm/models/_factory.py`](codebase/timm/models/_factory.py)
- [`codebase/timm/models/_registry.py`](codebase/timm/models/_registry.py)
- [`codebase/timm/models/_pretrained.py`](codebase/timm/models/_pretrained.py)
