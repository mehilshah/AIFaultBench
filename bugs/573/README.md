# Bug 573 Repro Bundle

This folder reproduces DeepSpeed issue [#7728](https://github.com/deepspeedai/DeepSpeed/issues/7728).

The bug is in `UlyssesSPAttentionHF.register_with_transformers` inside
[`codebase/deepspeed/runtime/sequence_parallel/ulysses_sp.py`](codebase/deepspeed/runtime/sequence_parallel/ulysses_sp.py).
The function only treats `transformers.PreTrainedModel` as an already-loaded model, so a PEFT wrapper is
sent to `AutoConfig.from_pretrained(...)` and fails.

## Files

- [`repro.py`](repro.py)
- [`requirements.txt`](requirements.txt)
- [`setup_env.sh`](setup_env.sh)
- [`run_repro.sh`](run_repro.sh)
- [`manifest.json`](manifest.json)
- [`reproduction.json`](reproduction.json)
- [`repro_stdout.log`](repro_stdout.log)
- [`repro_stderr.log`](repro_stderr.log)

## Repro

1. Run `bash setup_env.sh`
2. Run `bash run_repro.sh`

The repro uses:

- CPU-only `torch`
- `transformers==4.51.3`
- `peft`
- the local DeepSpeed source in `codebase/`

Expected result: `register_with_transformers(...)` raises while handling the PEFT model.
