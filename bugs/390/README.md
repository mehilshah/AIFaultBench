# Bug 390

This folder is a reusable repro bundle for the CANINE fp16 ONNX export bug.

Reused inputs:
- `bug_report.txt`
- `codebase/` at `b70d02fc724d04c916832ca4ead03ff05e8fb1ee`

Reproduction artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction summary:
- `CanineModel(...).half()` fails during ONNX tracing with `RuntimeError: expected m1 and m2 to have the same dtype, but got: float != c10::Half`
- The issue reproduces with a reduced local CANINE config, so no Hub download is required

To recreate the environment:
`bash setup_env.sh`

To run the repro:
`bash run_repro.sh`
