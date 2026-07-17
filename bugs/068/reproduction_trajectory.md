# Reproduction Trajectory — Bug 068: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1475](https://github.com/keras-team/keras-io/issues/1475)
- **Repository:** keras-team/keras-io @ `f0ec3b083a4ccedc65f371a2aaa9de86df9142bb`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a BoxCOCOMetrics instance with bounding_box_format='xyxy' and a very large evaluate_freq.
2. Call update_state() twice with two synthetic batches whose box tensors have shapes [4, 2, 4] and [4, 1, 4].
3. Call result(force=True) after the second update and observe the tf.concat shape mismatch.

## Observed behavior

- With tensorflow-cpu==2.21.0 and keras-cv==0.9.0, ./run_repro.sh exits 1. The metric crashes in BoxCOCOMetrics.result(force=True) with InvalidArgumentError: ConcatOp : Dimension 1 in both shapes must be equal: shape[0] = [4,2,4] vs. shape[1] = [4,1,4].

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
