# Bug 631

Reproduction for SDV issue 2701: `SingleTableDayZSynthesizer.validate_parameters` does not reject an invalid `DAYZ_SPEC_VERSION`.

Files:
- `repro.py` reproduces the validation call
- `requirements.txt` installs the local `codebase/` editable package
- `setup_env.sh` installs dependencies
- `run_repro.sh` executes the repro
- `reproduction.json` is written after reproduction

Expected behavior:
- validation should raise an error when `DAYZ_SPEC_VERSION` is not the expected spec version

Observed behavior in this checkout:
- validation currently accepts `DAYZ_SPEC_VERSION = 'V1000'`
- `bash run_repro.sh` prints:
  - `NO_ERROR`
  - `V1000`
