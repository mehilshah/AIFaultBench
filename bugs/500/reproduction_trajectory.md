# Reproduction Trajectory — Bug 500: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1196](https://github.com/huggingface/accelerate/issues/1196)
- **Repository:** huggingface/accelerate @ `d1aa558119859c4b205a324afabaecabd9ef375e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install the minimal dependency set.
2. Load the real launcher from codebase/src/accelerate/commands/launch.py with TPU config defaults.
3. Call _validate_launch_command; it dereferences defaults.tpu_cluster and raises AttributeError.

## Observed behavior

- AttributeError at codebase/src/accelerate/commands/launch.py:793: 'ClusterConfig' object has no attribute 'tpu_cluster'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
