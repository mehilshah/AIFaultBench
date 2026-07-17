# Bug 530

Repro bundle for JAX issue 38100.

Bug summary:
- `jax.jit(lambda x: jnp.log2(jnp.exp2(x)))` is rewritten to `x`
- this hides `exp2` overflow at `x = 128.0` for `float32`
- it also hides float32 round-trip error at smaller values such as `x = 13.0`

Reproduced with:
- `jax==0.10.2`
- `jaxlib==0.10.1`
- `numpy==2.2.6`
- `ml_dtypes==0.5.4`
- `opt_einsum==3.4.0`
- `scipy==1.18.0`

Artifacts in this folder:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `manifest.json`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run:
```bash
bash run_repro.sh
```
