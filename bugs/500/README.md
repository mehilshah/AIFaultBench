# Bug 500

This folder contains a self-contained reproduction bundle for
`https://github.com/huggingface/accelerate/issues/1196`.

Reproduction approach:
- Load the real launcher implementation from `codebase/src/accelerate/commands/launch.py`.
- Use the TPU config shape from the report.
- Trigger `_validate_launch_command`, which reads `defaults.tpu_cluster` even though `ClusterConfig` only exposes `tpu_use_cluster`.

Generated artifacts:
- `repro.py`
- `tpu_config.yaml`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`
