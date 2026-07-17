# Reproduction Trajectory — Bug 283: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47332](https://github.com/huggingface/transformers/issues/47332)
- **Repository:** huggingface/transformers @ `498d6e984e84d29186e671656817a53a024af930`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a tiny local Qwen3VL checkpoint from config.
2. Reload it with device_map='auto' and max_memory={'cpu': '50KB'} to force CPU/disk offloading.
3. Call save_pretrained() on the offloaded model.

## Observed behavior

- A mixed CPU/disk-offloaded Qwen3VL checkpoint loads and saves successfully in this checkout. The repro emits a warning about offloaded modules and writes model.safetensors without error.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The current codebase already handles saving a mixed CPU/disk-offloaded Qwen3VL model, so the reported meta-tensor failure does not occur here.
