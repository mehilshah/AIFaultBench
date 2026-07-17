# Reproduction Trajectory — Bug 105: vector-quantize-pytorch

- **Bug report:** [https://github.com/lucidrains/vector-quantize-pytorch/issues/142](https://github.com/lucidrains/vector-quantize-pytorch/issues/142)
- **Repository:** lucidrains/vector-quantize-pytorch @ `133f7386df6cf83345bb7cddca741d0364753af1`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a local virtual environment and install torch, einops, and einx.
2. Run the standalone harness against the local code snapshot.
3. Inspect the stdout/stderr logs for any shape mismatch traceback.

## Observed behavior

- The default single-process stress run using the issue's ResidualVQ settings completed 20 iterations without raising the reported shape mismatch.
- The harness printed repro_not_triggered at the end of the run.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported RuntimeError did not reproduce in this environment during the local single-process stress run.
