# Reproduction Trajectory — Bug 560: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7729](https://github.com/deepspeedai/DeepSpeed/issues/7729)
- **Repository:** microsoft/DeepSpeed @ `d568375e5bd50e4e5fd5e4c011e7be5982ecd528`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a CPU-only virtualenv and installed torch 2.6.0+cpu plus transformers 4.53.3, peft 0.16.0, and DeepSpeed runtime dependencies.
2. Launched the repro under 2 distributed CPU ranks with `run_repro.sh`.
3. Observed the expected OSError when `UlyssesSPAttentionHF.register_with_transformers()` received a PEFT-wrapped model object instead of a path or PreTrainedModel.

## Observed behavior

- run_repro.sh completed with rank-0 stdout showing exception_type=OSError and exception_message=Can't load the configuration of a PeftModelForCausalLM object; stderr shows the traceback ending at deepspeed/runtime/sequence_parallel/ulysses_sp.py:397 in AutoConfig.from_pretrained(model_name_or_path).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
