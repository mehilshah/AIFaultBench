# Pyro `AutoNormal.quantiles()` shape bug

This folder reproduces [pyro-ppl/pyro#2870](https://github.com/pyro-ppl/pyro/issues/2870).

The bug is in `AutoNormal.quantiles()`: when a latent site has a vector shape, the code passes a 1D tensor of quantile probabilities directly into `torch.distributions.Normal.icdf()`, which triggers a broadcast mismatch.

## Files

- `repro.py`: minimal failing script
- `requirements.txt`: runtime dependencies pinned for this repro
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the reproducer
- `manifest.json`: bundle metadata

## Expected result

Running the repro should fail with:

`RuntimeError: The size of tensor a (85) must match the size of tensor b (3) at non-singleton dimension 0`

## Run

```bash
./setup_env.sh
./run_repro.sh
```
