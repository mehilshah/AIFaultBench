# Bug 451 Repro

This folder reproduces the Lightning CLI validation bug reported in:
`https://github.com/Lightning-AI/pytorch-lightning/issues/21580`

The checked out source tree is pinned to:
`283ce7733ec23786d41751f185093eac83c0ef8d`

Reproduction summary:
- `lightning.pytorch.strategies.FSDPStrategy` advertises `device_mesh: Optional[Union[tuple[int], "DeviceMesh"]]`
- the CLI parser rejects the reported YAML value `device_mesh: [1, 4]`
- the failure occurs before any training code runs

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
`bash run_repro.sh`
