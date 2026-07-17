# Bug 452

Source issue: `https://github.com/huggingface/accelerate/issues/1400`

This folder contains a self-contained reproduction bundle for the empty-dataloader shard bug in `accelerate`.

What is included:
- `bug_report.txt`: the recovered issue report
- `codebase/`: the checked-out `huggingface/accelerate` source at `fafadc532351f3434f4d4abd4b61d356932607d8`
- `repro.py`: a minimal driver that exercises the batch dispatcher logic
- `requirements.txt`: runtime dependencies for the repro environment
- `setup_env.sh`: creates a clean venv and installs dependencies
- `run_repro.sh`: runs the repro once the environment is ready
- `reproduction.json`: schema-constrained result written after running the repro
- `repro_stdout.log` and `repro_stderr.log`: captured command output from the final run

Observed behavior in this folder:
- a single iterable sample is expanded to a batch of size 2
- when split across 4 processes, ranks 2 and 3 receive empty tensors

Reproduction command:
`bash run_repro.sh`
