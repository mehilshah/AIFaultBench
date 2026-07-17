# Bug 209

This folder contains a standalone reproduction bundle for the `FqnToConfig` / QAT module-swap bug reported in
[`bug_report.txt`](bug_report.txt).

What reproduces:
- `quantize_(m, FqnToConfig({"l": QATConfig(..., step="prepare")}), filter_fn=None)` leaves `m.l` as
  `torch.nn.Linear` instead of swapping it to the QAT module.
- The issue reproduces on CPU with PyTorch 2.8.0+cpu and `numpy`.

Generated artifacts:
- [`repro.py`](repro.py)
- [`requirements.txt`](requirements.txt)
- [`setup_env.sh`](setup_env.sh)
- [`run_repro.sh`](run_repro.sh)
- [`reproduction.json`](reproduction.json)
- [`repro_stdout.log`](repro_stdout.log)
- [`repro_stderr.log`](repro_stderr.log)

Run:
```bash
bash run_repro.sh
```

Reproduction command recorded in the result JSON:
- `bash run_repro.sh`

Source inputs:
- issue URL: `https://github.com/pytorch/ao/issues/3490`
- bug report source: `bug_report.txt`
- codebase source: `codebase/`
