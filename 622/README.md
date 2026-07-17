# Bug 622

Reproduction bundle for huggingface/diffusers issue [#13477](https://github.com/huggingface/diffusers/issues/13477).

## What fails

`ErnieImagePipeline.__call__` builds `callback_kwargs` with:

```python
callback_kwargs = {k: locals()[k] for k in callback_on_step_end_tensor_inputs}
```

On Python 3.10, this raises `KeyError: 'latents'` when `callback_on_step_end_tensor_inputs=["latents"]`.

## Repro strategy

The repro uses:

- local source from `codebase/`
- a tiny dummy pipeline setup
- `prompt_embeds` instead of model downloads
- `output_type="latent"` so decoding is skipped

That keeps the reproduction fast and deterministic while still hitting the failing callback line in the real pipeline code.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

Expected result:

- `repro_stdout.log` shows the pipeline setup and call
- `repro_stderr.log` ends with `KeyError: 'latents'`
