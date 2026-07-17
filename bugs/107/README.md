# Bug 107 Reproduction

This bundle reproduces the `adapters` import failure reported in
https://github.com/adapter-hub/adapters/issues/748.

## What it does

`repro.py` imports `LoRAConfig` from the local `codebase/src` checkout while
`huggingface-hub==0.26.0` is installed. That import path reaches
`adapters.utils`, which still imports `url_to_filename` from
`huggingface_hub.file_download`.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The failing traceback is written to:

- `repro_stdout.log`
- `repro_stderr.log`

