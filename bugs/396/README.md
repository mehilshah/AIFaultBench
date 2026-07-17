# Bug 396

AdaLoRA crashes when `lora_dropout=0` because `update_layer()` inserts a plain Python function into `nn.ModuleDict` instead of a module.

## Reproduction

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro is self-contained:

- `repro.py` uses a tiny in-memory BERT sequence-classification model.
- `run_repro.sh` points `PYTHONPATH` at `codebase/src`.
- `requirements.txt` pins the minimum dependency set that worked in this folder.

## Evidence

The failure is raised in `codebase/src/peft/tuners/adalora.py:342-352` with:

`TypeError: peft.tuners.adalora.AdaLoraLayer.update_layer.<locals>.lora_dropout_layer is not a Module subclass`

## Source

- issue URL: `https://github.com/huggingface/peft/issues/730`
- commit hash: `30fd5a4c88db369e87eab27ebf01c0b28bed02dc`
- library: `peft`
- library version: `0.5.0.dev0`
