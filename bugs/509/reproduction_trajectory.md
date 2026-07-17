# Reproduction Trajectory — Bug 509: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3143](https://github.com/pyro-ppl/pyro/issues/3143)
- **Repository:** pyro-ppl/pyro @ `aab99f8a693943a95fb3380838bb6b56e77e677e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a top-level Pyro model and wrap it in a class that owns one MCMC(NUTS(model), num_samples=2, warmup_steps=2, num_chains=2, mp_context='spawn', disable_progbar=True) instance.
2. Call holder.fit(torch.tensor(0.0)) twice in the same process.
3. Observe the second call raise ValueError: bad value(s) in fds_to_keep from multiprocessing spawn.

## Observed behavior

- Running the same MCMC instance twice with num_chains=2 and mp_context='spawn' succeeds on the first call and fails on the second call with ValueError: bad value(s) in fds_to_keep.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
