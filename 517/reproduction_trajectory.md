# Reproduction Trajectory — Bug 517: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3068](https://github.com/pyro-ppl/pyro/issues/3068)
- **Repository:** pyro-ppl/pyro @ `611dda1f2e0060af93b329ad1f196788635424b6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Monkeypatched torch.__version__ before importing pyro so the local checkout would load under the installed Torch build.
2. Ran the tutorial-style GMM model with AutoDelta globals and an enumerated local assignment guide.
3. Measured current RSS during 1000 Trace_ELBO steps and 1500 TraceEnum_ELBO steps.
4. Observed monotonic RSS growth only on TraceEnum_ELBO after the initial allocator jump.

## Observed behavior

- TraceEnum_ELBO on the tutorial-style GMM increased RSS from 783472 KB to 786844 KB between steps 500 and 1500 (+3372 KB), while the same model/guide under Trace_ELBO stayed flat at 782328 KB -> 782328 KB (+0 KB).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
