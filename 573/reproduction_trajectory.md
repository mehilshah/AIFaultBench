# Reproduction Trajectory — Bug 573: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7728](https://github.com/deepspeedai/DeepSpeed/issues/7728)
- **Repository:** microsoft/DeepSpeed @ `d568375e5bd50e4e5fd5e4c011e7be5982ecd528`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local virtualenv with `bash setup_env.sh`.
2. Run the distributed repro with `bash run_repro.sh`.
3. Observe the traceback showing the PEFT model is not a `PreTrainedModel` and DeepSpeed falls through to `AutoConfig.from_pretrained(...)` on the wrapper object.

## Observed behavior

- Running the repro on 2 CPU ranks with a real PEFT-wrapped `PeftModelForCausalLM` prints `isinstance_pretrained=False` and then fails inside `UlyssesSPAttentionHF.register_with_transformers(...)` at `codebase/deepspeed/runtime/sequence_parallel/ulysses_sp.py:397`, where `AutoConfig.from_pretrained(model_name_or_path)` is called on the PEFT object and raises `OSError` after `HFValidationError` because the wrapper is not treated as an already-loaded model.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
