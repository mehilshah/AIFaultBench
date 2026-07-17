# Reproduction Trajectory — Bug 622: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13477](https://github.com/huggingface/diffusers/issues/13477)
- **Repository:** huggingface/diffusers @ `c41a3c3ed8ab16d4fadd2f08ee0f49cb78e79994`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. bash setup_env.sh
2. bash run_repro.sh
3. Observe repro_stderr.log ending with KeyError: 'latents' and the traceback pointing at pipeline_ernie_image.py:355

## Observed behavior

- On Python 3.10.13 with torch 2.13.0+cpu, the real ErnieImagePipeline call reaches codebase/src/diffusers/pipelines/ernie_image/pipeline_ernie_image.py:355 and raises KeyError: 'latents' from callback_kwargs = {k: locals()[k] for k in callback_on_step_end_tensor_inputs}.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
