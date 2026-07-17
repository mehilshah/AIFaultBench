# Bug 075 Reproduction

Issue: [DeepSpeedExamples #847](https://github.com/deepspeedai/DeepSpeedExamples/issues/847)

Reported failure:
`ParquetConfig.__init__() got an unexpected keyword argument 'token'`

What I verified:
- The GPT-2 XL autotuning script in `codebase/training/autotuning/hf/gpt2-xl/test_tune.sh` forwards `token=` into the Hugging Face `load_dataset(...)` call.
- On the closest compatible package set I could run locally, the same `token` path does **not** raise the reported `ParquetConfig` error.
- I therefore marked this bug as **not reproducible in this folder/environment**.

Bundle contents:
- `repro.py` - minimal token-forwarding dataset load check
- `requirements.txt` - pinned reproduction environment
- `setup_env.sh` - creates a local virtual environment and installs dependencies
- `run_repro.sh` - runs the repro and captures stdout/stderr
- `reproduction.json` - schema-constrained result record

Run locally:
```bash
./run_repro.sh
```

The script writes logs to:
- `repro_stdout.log`
- `repro_stderr.log`

