# Bug 442

This folder contains the standardized input and the reproduction bundle
for Detectron2 issue #642.

What was checked:
- the issue-reported training recipe from `bug_report.txt`
- the checked-out source tree in `codebase/`
- the `ImageList.from_tensors` single-image path that was fixed in commit `abae3ae`

Result:
- the bug is not reproducible in this folder because the checked-out codebase
  already contains the fix that avoids mutating the zero-padding single-image path
- the original report requires a full COCO training/eval run, which is not
  available in this standardized folder

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
