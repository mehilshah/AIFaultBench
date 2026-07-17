# Bug 473

Repro bundle for numpyro issue [2055](https://github.com/pyro-ppl/numpyro/issues/2055).

## What fails

With `flax==0.11.0`, constructing the NNX dropout module with only a `params`
RNG stream raises:

`KeyError: "No RngStream named 'dropout' found in Rngs."`

The failure appears in both smoke-test variants from
`test/contrib/test_module.py`:

- `test_nnx_state_dropout_smoke[no_batchnorm-dropout]`
- `test_nnx_state_dropout_smoke[batchnorm-dropout]`

## Files

- `repro.py`: minimal failing script
- `requirements.txt`: pinned repro dependencies
- `setup_env.sh`: creates a local virtualenv and installs dependencies
- `run_repro.sh`: runs the repro inside the virtualenv

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```
