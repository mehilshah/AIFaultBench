# Bug 321 Reproduction Bundle

This folder contains a self-contained reproduction of the PiSSA adapter interaction bug from
https://github.com/huggingface/peft/issues/2184.

## What it shows

Loading a PiSSA adapter mutates the shared base model weights. If a non-PiSSA adapter was already loaded, re-activating
that earlier adapter changes its output.

## Files

- `repro.py`: runs the minimal reproduction on a tiny `nn.Linear` model.
- `requirements.txt`: dependency list for a clean environment.
- `setup_env.sh`: creates a venv and installs dependencies plus the local `codebase/`.
- `run_repro.sh`: executes the repro inside the prepared venv.
- `manifest.json`: metadata for the standardized folder.
- `reproduction.json`: JSON summary of the reproduction outcome.
- `repro_stdout.log` and `repro_stderr.log`: captured command output from the repro run.

## Expected result

The repro is considered successful when the non-PiSSA adapter output changes after the PiSSA adapter is loaded and the
base layer weight also changes.
