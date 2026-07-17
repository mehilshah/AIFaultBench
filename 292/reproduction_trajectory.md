# Reproduction Trajectory — Bug 292: torchrl

- **Bug report:** [https://github.com/pytorch/rl/issues/3881](https://github.com/pytorch/rl/issues/3881)
- **Repository:** pytorch/rl @ `6364a19bc97efadd62c9302a56e854e2c90d5edf`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a venv with system site packages so the preinstalled torch could be reused.
2. Installed the runtime dependencies needed for the local torchrl source: tensordict and open_spiel.
3. Ran repro.py with PYTHONPATH pointing at codebase/ and observed the expected ValueError during OpenSpielEnv construction.

## Observed behavior

- OpenSpielEnv("chess", return_state=True, batch_size=(100,)) raises ValueError during construction: "The value of spec.shape (torch.Size([1])) must match the env batch size (torch.Size([100]))." The exception is thrown from torchrl/envs/libs/openspiel.py while assigning done_spec, before reset() runs.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
