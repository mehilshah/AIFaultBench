# Reproduction Trajectory — Bug 342: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3301](https://github.com/pyro-ppl/pyro/issues/3301)
- **Repository:** pyro-ppl/pyro @ `a14fabc980ef115f499c89ffb242cbba8555e824`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a fresh Python 3.12 virtual environment.
2. Installed torch 2.5.1+cpu and the local dependency set.
3. Restored the local Pyro source tree into codebase/.
4. Ran the issue snippet against the restored local Pyro code.
5. Observed that gate_logits behaves like gate and the bug does not reproduce.

## Observed behavior

- In a clean venv with the restored local codebase, ZeroInflatedPoisson(rate=100, gate_logits=log(p/(1-p))) reported zip_from_logits.gate=0.300000 and sampled zero_fraction_gate_logits=0.306000, while the gate=0.3 path produced zero_fraction_gate=0.297000.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The restored local code snapshot already includes the fixed binary-logit handling in pyro/distributions/zero_inflated.py, so the reported bug is not present here.
