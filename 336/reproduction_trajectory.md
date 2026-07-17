# Reproduction Trajectory — Bug 336: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/48124](https://github.com/vllm-project/vllm/issues/48124)
- **Repository:** vllm-project/vllm @ `b83be00cddf03387bf740acfe6b9ca07ec1a3c08`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Inspect vllm/model_executor/models/deepseek_v2.py.
2. Compare pre-fix and current aux-hidden-state capture behavior with a 1-layer simulation.
3. Confirm that the current tree already appends the final layer hidden state after the loop.

## Observed behavior

- Source check: codebase/vllm/model_executor/models/deepseek_v2.py contains the final-layer capture branch: True.
- Pre-fix simulation for num_layers=1, aux_layers=(1,): [].
- Current/fixed simulation for num_layers=1, aux_layers=(1,): ['layer_1'].
- The fixed path captures the last layer auxiliary hidden state, so the reported bug is not reproducible in this tree.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The checked-in DeepSeek V2 implementation already includes the post-loop end-layer aux hidden-state capture that the bug report proposes.
