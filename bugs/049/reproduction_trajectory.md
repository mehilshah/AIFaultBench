# Reproduction Trajectory — Bug 049: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/4622](https://github.com/facebookresearch/fairseq/issues/4622)
- **Repository:** facebookresearch/fairseq @ `4fe8583396191c22011350248119db98ec1b5cb8`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Read the issue report and inspected fairseq/modules/espnet_multihead_attention.py.
2. Loaded the module directly from the local codebase with a minimal import shim.
3. Instantiated RelPositionMultiHeadedAttention and checked the relative-position bias tensors.
4. Confirmed the local snapshot already initializes both biases with Xavier.

## Observed behavior

- Loaded RelPositionMultiHeadedAttention from the local codebase.
source_uses_xavier=True
source_uses_raw_allocation=True
pos_bias_u_finite=True
pos_bias_v_finite=True
pos_bias_u_nonzero=True
pos_bias_v_nonzero=True
Result: the reported uninitialized-bias bug does not reproduce in this snapshot because the biases are initialized before use.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local fairseq snapshot already contains the fix: both relative-position bias parameters are initialized with Xavier uniform after allocation, so the uninitialized-bias behavior from the issue report is not present.
