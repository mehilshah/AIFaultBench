# Reproduction Bundle

This folder reproduces the tied-weight regression reported in
`huggingface/accelerate#993`.

## What fails

`dispatch_model()` breaks the alias between a tied embedding and output head
when the tied embedding is offloaded to `disk`. After dispatch, both
`embed_tokens.weight` and `lm_head.weight` appear separately in
`named_parameters()`.

## Files

- `repro.py`: minimal tied-weight model that triggers the bug
- `requirements.txt`: runtime dependencies for the repro
- `setup_env.sh`: creates a local venv and installs the package under test
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` and `repro_stderr.log`
- `manifest.json`: metadata for the bundle

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

Expected result in a healthy implementation:

- `post_dispatch_shared: True`
- `named_parameters()` should not add a second `lm_head.weight`

Observed locally in this snapshot:

- `post_dispatch_shared: False`
- `post_dispatch_named_parameters` includes both `embed_tokens.weight` and `lm_head.weight`
