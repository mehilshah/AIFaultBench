# Bug 613 Reproduction

This bundle reproduces the Gemma 4 `expert_weights` AttributeError described in `bug_report.txt`.

Relevant source locations:
- `codebase/vllm/model_executor/models/gemma4.py`
- `codebase/vllm/model_executor/models/gemma4_unified.py`

Observed mismatch:
- `Gemma4ForCausalLM` does not assign `self.expert_weights` during initialization.
- `Gemma4ForConditionalGeneration` / the unified wrapper dereferences `self.language_model.expert_weights`.

Run:

```bash
bash run_repro.sh
```

The command writes:
- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`
