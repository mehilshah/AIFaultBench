# Reproduction Trajectory — Bug 022: tensorflow/models

- **Bug report:** [https://github.com/tensorflow/models/issues/10980](https://github.com/tensorflow/models/issues/10980)
- **Repository:** tensorflow/models @ `5d10b3bca66a2a1acc01099ba6af420ca77fd7be`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Inspect official/vision/ops/augment.py::_parse_policy_info in the local codebase.
2. Run deterministic sampling with two different level_std values using the buggy logic.
3. Observe that the output sequences are identical and the measured standard deviation does not change.

## Observed behavior

- The source still contains `level += tf.random.normal([], dtype=tf.float32)` inside `_parse_policy_info`, so `level_std` is never used as the Gaussian scale. With the same seed, sampling with `level_std=0.25` and `level_std=2.5` produced identical outputs (5000 / 5000 values equal), with pstdev=1.026028 for both runs.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
