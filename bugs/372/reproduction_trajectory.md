# Reproduction Trajectory — Bug 372: pyro

- **Bug report:** [https://github.com/pyro-ppl/pyro/issues/3274](https://github.com/pyro-ppl/pyro/issues/3274)
- **Repository:** pyro-ppl/pyro @ `c00bcc3fb701327b07e94de88754da49b7f29ebe`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a Python 3.11 virtual environment with setup_env.sh.
2. Install numpy<2, torch==2.0.1, pyro-api, opt_einsum, and tqdm, then install the local codebase in editable mode.
3. Run repro.py through run_repro.sh and observe both the missing-support failure and the rsample shape failure.

## Observed behavior

- AutoNormal(model_with_MixtureOfDiagNormals) raises NotImplementedError when accessing site['fn'].support.
- MixtureOfDiagNormals.rsample(torch.Size([2, 3])) raises RuntimeError in _MixDiagNormalSample.forward with a tensor expansion shape mismatch.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
