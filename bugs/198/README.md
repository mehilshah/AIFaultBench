# Bug 198

This folder is a reusable reproduction bundle for the H5 scanning crash in `modelscan`.

Reproduction summary:
- A valid HDF5 file with no `model_config` attribute causes `modelscan` to raise `TypeError: the JSON object must be str, bytes or bytearray, not dict`.
- The failure happens in `modelscan/scanners/h5/scan.py` when `json.loads()` is called on the default `{}` value returned by `attrs.get("model_config", {})`.

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

How to reproduce:
1. Run `bash setup_env.sh` to create `.venv` and install the Python dependencies.
2. Run `bash run_repro.sh`.
3. Inspect `reproduction.json` and the log files.

Direct CLI equivalent:
`PYTHONPATH=codebase python3 -m modelscan.cli -p <path-to-h5-file>`
