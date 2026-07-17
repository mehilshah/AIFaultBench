# Reproduction Trajectory — Bug 497: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46858](https://github.com/huggingface/transformers/issues/46858)
- **Repository:** huggingface/transformers @ `d87f670d5b23860b5937473a5fddbba9d675780a`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local .venv with the CPU torch wheel and the small dependency set inferred from the bug report and codebase.
2. Installed the checked-out codebase in editable mode with --no-deps so the repro used this folder's transformers sources.
3. Ran run_repro.sh, which loads pretrained gpt2, sets generation_config.cache_implementation="static", compiles model.forward with torch.compile(backend="inductor"), and calls generate() twice.
4. Confirmed that both generate() calls succeeded without the reported crash.

## Observed behavior

- Running the exact GPT-2 repro from the issue against the local editable checkout on CPU with torch 2.10.0+cpu completed both model.generate() calls successfully. The captured output shows first_output_shape=(1, 3) and second_output_shape=(1, 3), both with the same token ids, and the script printed repro_status=not_reproduced.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported failure could not be triggered in this checkout. On CPU with torch 2.10.0+cpu, the exact issue sequence completed normally, so there is no crash to capture.
