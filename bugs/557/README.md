# Bug 557 Repro

Source inputs:
- `bug_report.txt`
- `codebase/`

What this repro checks:
- The default `UNet1DModel` config produces identical outputs for different timesteps, which matches the "time blind" behavior in the report.
- The no-skip variant from the report produces different outputs for different timesteps.

Notes:
- The issue report uses `sample_size=64`, but that configuration hits an unrelated padding error in this checkout.
- The repro uses `sample_size=1024` so the forward pass is valid and the timestep behavior can be compared directly.

Files in this bundle:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
`bash run_repro.sh`
