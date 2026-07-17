# PEFT merge_and_unload repro

This bundle reproduces the offload/merge/save failure from PEFT issue 868 on a tiny public model.

## What it does

- Loads `sshleifer/tiny-gpt2`
- Dispatches one transformer block to disk so the model contains meta tensors
- Adds a LoRA adapter
- Calls `merge_and_unload()`
- Calls `save_pretrained()` on the merged model

## Result

`save_pretrained()` fails with:

`TypeError: 'NoneType' object is not subscriptable`

The failure happens inside `transformers.integrations.accelerate.load_offloaded_parameter()` while saving a merged model that still has offloaded parameters.

## Run

```bash
./run_repro.sh
```

Outputs are written to:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`
