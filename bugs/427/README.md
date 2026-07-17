# Bug 427 Reproduction Bundle

This folder contains a self-contained reproduction of the timm DINOv3 bug reported in:
`https://github.com/huggingface/pytorch-image-models/issues/2593`

Observed failure in the referenced commit:
`AttributeError: 'RotaryEmbeddingDinoV3' object has no attribute 'update_feat_shape'`

Artifacts:
- `bug_report.txt`: source issue description
- `codebase/`: local checkout of `huggingface/pytorch-image-models@0645384b3a68d0ddf4657400125bb2c68c42bc60`
- `repro.py`: minimal reproducer
- `requirements.txt`: Python dependencies for the reproducer
- `setup_env.sh`: creates an isolated venv and installs dependencies
- `run_repro.sh`: runs the repro
- `reproduction.json`: schema-constrained result
- `repro_stdout.log`, `repro_stderr.log`: captured output from the repro run

The bug reproduces without pretrained weights. The minimal trigger is creating
`vit_base_patch16_dinov3.lvd1689m` and calling `set_input_size(512)`.
