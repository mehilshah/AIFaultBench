# Bug 011

This folder contains a self-contained reproduction harness for
`https://github.com/tensorflow/models/issues/11121`.

What is included:
- `bug_report.txt`
- `codebase/` snapshot from the issue bundle
- reproduction artifacts generated in this folder

Current verdict:
- The reported NaN loss is not reproducible in this environment.
- A 100-step `resnet_rs_imagenet`-style training run completes with finite loss.
- The run does diverge numerically, but it does not hit NaN here.

How to run:
- `bash run_repro.sh`

Notes:
- The bundled snapshot is Python 3.11 bytecode, so the repro uses `python3.11`.
- The loader shim in `pyc_loader.py` imports the source-less `codebase/` tree.
