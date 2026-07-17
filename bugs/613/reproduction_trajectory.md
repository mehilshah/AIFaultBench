# Reproduction Trajectory — Bug 613: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/46948](https://github.com/vllm-project/vllm/issues/46948)
- **Repository:** vllm-project/vllm @ `6eb63a1da6996abad00323dc7e845dc868996524`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash run_repro.sh` in the standardized bug folder.
2. Inspect `repro_stdout.log` and `repro_stderr.log` for the AttributeError.
3. Verify the source mismatch between `gemma4.py` and `gemma4_unified.py`.

## Observed behavior

- repro_stdout.log shows the source mismatch (`gemma4_has_expert_weights_assignment: false` and `gemma4_unified_accesses_expert_weights: true`) and the AttributeError when `Gemma4ForConditionalGeneration` dereferences `Gemma4ForCausalLM.expert_weights`; `codebase/vllm/model_executor/models/gemma4_unified.py:338` dereferences `self.language_model.expert_weights`; `codebase/vllm/model_executor/models/gemma4.py:1535-1573` initializes MoE metadata but never assigns `self.expert_weights`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
