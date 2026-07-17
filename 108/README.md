# Bug 108

Reproduction bundle for Hugging Face Transformers issue 42502.

Observed failure:

- `DataCollatorWithFlattening` raises `TypeError('can only concatenate list (not "Tensor") to list')` when `labels` are `torch.Tensor` objects.
- The same collator works when `labels` are Python lists.

Files in this bundle:

- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally:

```bash
bash run_repro.sh
```

The local source version is `5.0.0.dev0`, matching the checked-in repo state.
