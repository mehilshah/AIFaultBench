# Bug 561

This folder contains a self-contained reproduction bundle for
[`vllm-project/vllm#47054`](https://github.com/vllm-project/vllm/issues/47054).

## What the bundle does

- Reconstructs the source-derived cross-layer KV-cache packing layout described in the report.
- Records the local GPU/runtime environment.
- Marks the issue as not fully reproducible here because the machine is not the reported Hopper H100 setup and the full `vllm serve` + `lm_eval` workload was not executed.

## Files

- `repro.py`: generates the reproduction evidence and `reproduction.json`.
- `requirements.txt`: runtime dependencies for the repro harness.
- `setup_env.sh`: creates `.venv` and installs the requirements.
- `run_repro.sh`: runs the repro and captures `repro_stdout.log` / `repro_stderr.log`.
- `manifest.json`: metadata for the standardized bundle.
- `bug_report.txt`: original issue report.
- `codebase/`: local source tree used for the source-derived evidence.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
cat reproduction.json
```

## Reproduction command from the report

The reported runtime trigger is preserved in `repro.py` and matches the issue body:

- `vllm serve openai/gpt-oss-120b --tensor-parallel-size=2 --kv-transfer-config ...`
- `lm_eval --model local-completions ... --tasks gsm8k`
