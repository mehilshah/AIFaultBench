# Bug 022

Repro for TensorFlow Models issue 10980.

Bug summary:
- `official/vision/ops/augment.py::_parse_policy_info` accepts `level_std`
  but adds unit-variance Gaussian noise instead of scaling by `level_std`.
- Result: any non-zero `level_std` behaves the same as any other non-zero value.

Artifacts:
- `repro.py` - deterministic demonstration of the bug
- `requirements.txt` - no external dependencies required
- `setup_env.sh` - environment bootstrap stub
- `run_repro.sh` - executes the repro and captures logs
- `reproduction.json` - schema-constrained result
- `repro_stdout.log` / `repro_stderr.log` - captured command output

Reproduction command:
`bash run_repro.sh`
