# Reproduction Trajectory — Bug 256: sdv

- **Bug report:** [https://github.com/sdv-dev/SDV/issues/1741](https://github.com/sdv-dev/SDV/issues/1741)
- **Repository:** sdv-dev/SDV @ `6f8f50b`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a fresh Python 3.12 virtual environment.
2. Installed the runtime dependencies and the local SDV checkout in editable mode.
3. Ran the issue's minimal data/metadata setup for CTGANSynthesizer, TVAESynthesizer, and CopulaGANSynthesizer.
4. Observed that fit completed with has _model=False for each synthesizer.
5. Observed sample(10) raise AttributeError for each synthesizer.

## Observed behavior

- In a fresh Python 3.12 venv with the local SDV checkout installed editable, fitting a dataset whose metadata drops every modeled column left each synthesizer without _model. CTGANSynthesizer, TVAESynthesizer, and CopulaGANSynthesizer each failed on sample(10) with AttributeError: '...Synthesizer' object has no attribute '_model'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
