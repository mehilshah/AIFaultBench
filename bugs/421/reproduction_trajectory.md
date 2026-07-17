# Reproduction Trajectory — Bug 421: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13967](https://github.com/huggingface/diffusers/issues/13967)
- **Repository:** huggingface/diffusers @ `4757c7c465157ce843294424a5dd9fcd24f52cb2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Import the real `ErnieImageModularPipeline` class from `codebase/src` using a local `torch` stub.
2. Instantiate the class shell and call `load_lora_weights` on it.
3. Observe `AttributeError: 'ErnieImageModularPipeline' object has no attribute 'load_lora_weights'`.

## Observed behavior

- ErnieImageModularPipeline bases: ['ModularPipeline'] | ErnieImageModularPipeline defines methods: none | hasattr(ErnieImageModularPipeline, 'load_lora_weights') -> False | calling pipe.load_lora_weights(...) -> 'ErnieImageModularPipeline' object has no attribute 'load_lora_weights' | modular pipeline source shows `class ErnieImageModularPipeline(ModularPipeline)` at line 66 | non-modular pipeline source shows `class ErnieImagePipeline(DiffusionPipeline, ErnieImageLoraLoaderMixin)` at line 42

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
