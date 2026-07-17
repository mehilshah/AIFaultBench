# PEFT 4-bit LoRA init repro

This folder contains a standalone reproduction for the `olora` and `pissa` LoRA initialization path on a quantized 4-bit-like layer.

The repro uses:

- the local `codebase/` checkout
- a tiny fake `bitsandbytes` package to model the 4-bit API surface
- a custom module that keeps the base forward valid while exposing a flattened `1x1` quantized weight to the LoRA init code

Expected behavior:

- `init_lora_weights=True` should run
- `init_lora_weights="olora"` should fail in the first forward
- `init_lora_weights="pissa"` should fail in the first forward

Run:

```bash
bash setup_env.sh
bash run_repro.sh
```

