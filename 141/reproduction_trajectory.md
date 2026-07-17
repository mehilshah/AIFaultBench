# Reproduction Trajectory — Bug 141: safetensors

- **Bug report:** [https://github.com/huggingface/safetensors/issues/442](https://github.com/huggingface/safetensors/issues/442)
- **Repository:** huggingface/safetensors @ `b947b59`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local virtual environment and installed torch and numpy from requirements.txt.
2. Used the local codebase sources via PYTHONPATH to import safetensors.torch.
3. Generated a minimal safetensors file containing a single zero-length float32 tensor.
4. Verified that load_file() returned the expected tensor keys and shape, then confirmed that load(bytes) raised the reported ValueError.

## Observed behavior

- A safetensors file containing an empty float32 tensor loads successfully with safetensors.torch.load_file().
- Calling safetensors.torch.load() on the same file bytes raises ValueError: both buffer length (0) and count (-1) must not be 0.
- The traceback points to safetensors.torch._view2torch() calling torch.frombuffer(v["data"], dtype=dtype) on the empty tensor payload.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
