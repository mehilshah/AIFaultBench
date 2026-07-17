# Reproduction Trajectory — Bug 599: DeepSpeed

- **Bug report:** [https://github.com/deepspeedai/DeepSpeed/issues/7711](https://github.com/deepspeedai/DeepSpeed/issues/7711)
- **Repository:** microsoft/DeepSpeed @ `7f2f423257592725259a0950094dc9fe9d276a27`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load the real DeepSpeed launcher source from codebase/deepspeed/launcher/multinode_runner.py.
2. Construct an OpenMPIRunner with a two-host resource pool and no OMPI_* variables in the environment.
3. Observe the constructor raise OSError: MPI environment variables are not set.

## Observed behavior

- OpenMPIRunner raised OSError before mpirun launch: OSError: MPI environment variables are not set. Ensure you are running the script with an MPI-compatible launcher.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
