# Reproduction Trajectory — Bug 051: keras-io

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1840](https://github.com/keras-team/keras-io/issues/1840)
- **Repository:** keras-team/keras-io @ `3c4465806eef2129a4d7a09ed43ea451aa9c03f8`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local Python 3.12 virtualenv and installed keras==3.2.1, tensorflow==2.20.0, tensorflow-text==2.20.1, and keras-nlp==0.14.4.
2. Ran the minimal reproducer in repro.py through bash run_repro.sh.
3. Observed the reported TypeError at the GreedySampler call site.

## Observed behavior

- bash run_repro.sh exited with code 1. The captured stderr ends with TypeError: Sampler.__call__() got an unexpected keyword argument 'end_token_id'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
