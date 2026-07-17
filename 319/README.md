# Bug 319 Repro Bundle

This folder contains a self-contained reproduction bundle for:

- DeepSpeed issue: [#7942](https://github.com/deepspeedai/DeepSpeed/issues/7942)
- Reported failure: DeepCompile on `Qwen/Qwen1.5-MoE-A2.7B-Chat` raises `RuntimeError: 'weight' must be 2-D`

Files in this bundle:

- `repro.py` - runnable repro driver
- `requirements.txt` - Python dependencies for the repro environment
- `setup_env.sh` - creates a virtualenv and installs dependencies
- `run_repro.sh` - runs the repro and writes the result/log files
- `manifest.json` - metadata for this standardized bug folder
- `reproduction.json` - schema-constrained result written by the repro run
- `repro_stdout.log` / `repro_stderr.log` - captured command output

Run locally:

```bash
bash run_repro.sh
```

Behavior:

- If CUDA, DeepSpeed, and the Qwen2MoE stack are available, `repro.py` attempts the real DeepCompile path using a tiny Qwen2MoE config and compares it against a tiny LLaMA config.
- If the environment is missing the required GPU/runtime pieces, the script falls back to a shape-only reproduction that flattens `embed_tokens.weight` to the same bad 1-D shape that triggers the reported error.

The fallback reproduces the exact low-level exception, but it does not validate the full DeepCompile stack in this machine.
