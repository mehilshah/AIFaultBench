# Bug 201

This folder is a standalone reproduction bundle for the NumPyro issue reported in
`bug_report.txt`.

What is included:
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

Reproduction summary:
- library: `numpyro`
- snapshot version: `0.13.2`
- issue URL: `https://github.com/pyro-ppl/numpyro/issues/1713`
- observed failure: `KeyError: 'components'` in `numpyro/contrib/funsor/enum_messenger.py`

Run the repro with:
`bash run_repro.sh`
