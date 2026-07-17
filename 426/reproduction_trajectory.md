# Reproduction Trajectory — Bug 426: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/499](https://github.com/huggingface/peft/issues/499)
- **Repository:** huggingface/peft @ `3714aa2fff158fdfa637b2b65952580801d890b2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run `bash setup_env.sh` to create `.venv` and install the CUDA-capable torch wheel plus the pinned accelerate/transformers stack and editable PEFT checkout.
2. Run `bash run_repro.sh`.
3. The process exits with a device-mismatch RuntimeError in `peft_model.py` during `PromptEncoder` FSDP prompt-tuning forward.

## Observed behavior

- With the bundled repro on this Blackwell GPU, the forward pass fails inside `codebase/src/peft/peft_model.py`.
- Current observed traceback: `RuntimeError: Expected all tensors to be on the same device, but got tensors is on cuda:0, different from other tensors on cpu` at line 557 in the prompt-tuning forward path.
- The repro prints `accelerator.device=cuda`, `input_ids.device=cuda:0`, and `attention_mask.device=cuda:0` before the failure.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
