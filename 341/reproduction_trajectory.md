# Reproduction Trajectory — Bug 341: numpyro

- **Bug report:** [https://github.com/pyro-ppl/numpyro/issues/2132](https://github.com/pyro-ppl/numpyro/issues/2132)
- **Repository:** pyro-ppl/numpyro @ `43fa32ce00c293367ebafbfc4a047840906dcb8b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create the local venv and install JAX 0.9.0 CUDA 13 wheels plus the runtime dependencies.
2. Run the issue's GP-style NUTS benchmark with 4 vectorized chains on the local GPU.
3. Compare a post-warmup run on the same MCMC object against a fresh num_warmup=0 restart.
4. Repeat the comparison for a second steady-state batch after setting post_warmup_state.

## Observed behavior

- backend=gpu, device=cuda:0; warmup=13.662s; first post-warmup run same_object=7.645s vs fresh num_warmup=0=8.426s (ratio=0.91x); second batch same_object=3.770s vs fresh num_warmup=0=3.217s (ratio=1.17x).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported slowdown did not reproduce here; the same-object path was roughly equal to or slightly faster than the fresh num_warmup=0 path.
