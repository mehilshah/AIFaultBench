# Bug 577 Reproduction

This folder reproduces the JAX 0.6.0 and Haiku compatibility failure described in `bug_report.txt`.

The failing dependency combination is:
- `jax==0.6.0`
- `jaxlib==0.6.0`
- `dm-haiku==0.0.13`

The bug is an import-time break in Haiku:
- `haiku.__init__` pulls in `haiku.experimental.jaxpr_info`
- that module still references `jax.core.JaxprEqn`
- JAX 0.6.0 removed `jax.core.JaxprEqn` and raises `AttributeError`

The bundled NumPyro source tree is preserved for context, but the shortest runnable repro is a direct Haiku import under the pinned versions above.

## Usage

```bash
bash setup_env.sh
bash run_repro.sh
```

The repro command writes:
- `repro_stdout.log`
- `repro_stderr.log`

and records the final structured result in:
- `reproduction.json`
