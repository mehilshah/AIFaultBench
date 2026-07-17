# Reproduction Trajectory — Bug 272: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48700](https://github.com/vllm-project/vllm/issues/48700)
- **Repository:** vllm-project/vllm @ `3b39fd284aa3bcfcad57736cdd5ddb9eb4b746d2`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read vllm/v1/worker/gpu/spec_decode/eagle/utils.py from the local codebase.
2. Checked whether lm_head is resolved through the language-model submodule.
3. Confirmed the current snapshot does not match the vulnerable pattern from the bug report.

## Observed behavior

- inspected_file=codebase/vllm/v1/worker/gpu/spec_decode/eagle/utils.py fixed_lookup_present=True vulnerable_lookup_present=False The checked-in source already uses the language-model lm_head fallback, so the reported crash path is absent.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local source tree already contains the fix for the reported bug, so the original AttributeError cannot be reproduced here.
