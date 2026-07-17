# Bug 214

Reproduction bundle for SDV issue 2434.

## What this shows

The reported `regex_format` value `'(10|20|30)[0-9]{4}'` validates in metadata, but
`GaussianCopulaSynthesizer.fit()` still crashes while the regex is converted into an
`rdt.transformers.RegexGenerator`.

This bundle uses small import stubs for unrelated `ctgan` / `deepecho` modules so the
Gaussian-copula path can be exercised without the broken deep-learning stack.

## Files

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

## Run

```bash
bash run_repro.sh
```
