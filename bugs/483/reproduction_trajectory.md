# Reproduction Trajectory — Bug 483: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46877](https://github.com/huggingface/transformers/issues/46877)
- **Repository:** huggingface/transformers @ `9b6af5d77de78f0a57a098b2809009ad6ec0cfe3`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a clean virtual environment and installed the runtime dependencies listed in requirements.txt.
2. Ran PYTHONPATH=$PWD/codebase/src .venv/bin/python repro.py to import the three reported modules.
3. Observed that the import completed without emitting the [ERROR] doc-lint messages described in the report.

## Observed behavior

- In an isolated Python 3.12 venv with the repository's runtime dependencies installed, importing transformers.models.qwen2_5_vl.modeling_qwen2_5_vl, transformers.models.qwen3_vl.modeling_qwen3_vl, and transformers.models.glm.modeling_glm produced no stdout diagnostics.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The referenced commit snapshot does not reproduce the reported stdout leak during import.
