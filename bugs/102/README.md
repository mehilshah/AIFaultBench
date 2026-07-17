# Bug 102 Reproduction Bundle

This folder contains a standalone repro for:

- `vector_quantize_pytorch.residual_sim_vq.ResidualSimVQ.forward`
- issue: `NameError: name 'return_loss' is not defined`

## Contents

- `bug_report.txt`: recovered issue report
- `codebase/`: local source snapshot used for reproduction
- `repro.py`: minimal Python reproducer
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: environment bootstrap helper
- `run_repro.sh`: shell entrypoint for the repro
- `manifest.json`: standardized metadata for the bug folder
- `reproduction.json`: schema-constrained reproduction result
- `repro_stdout.log` / `repro_stderr.log`: captured command output

## Repro

The repro is expected to fail immediately when calling `ResidualSimVQ.forward`,
because the implementation references `return_loss` even though that name is not
defined in the method signature or body.

Run:

```bash
bash run_repro.sh
```
