# Bug 372

Reproduction bundle for https://github.com/pyro-ppl/pyro/issues/3274.

Confirmed behavior in this checkout:
- `AutoNormal` fails on `MixtureOfDiagNormals` because the distribution does not define `support`.
- `MixtureOfDiagNormals.rsample(torch.Size([2, 3]))` raises a shape mismatch in `_MixDiagNormalSample.forward` under Torch 2.0.1 / Pyro 1.8.6.

Files in this folder:
- `bug_report.txt`
- `codebase/`
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
