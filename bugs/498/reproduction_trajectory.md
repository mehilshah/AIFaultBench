# Reproduction Trajectory — Bug 498: diffusers

- **Bug report:** [https://github.com/huggingface/diffusers/issues/13819](https://github.com/huggingface/diffusers/issues/13819)
- **Repository:** huggingface/diffusers @ `ff3b86b4755b46a7b5656dfcf84d25bd25ad4740`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Load QwenImageEditPipeline from Qwen/Qwen-Image-Edit with torch.bfloat16.
2. Run the documentation snippet against the yarn-art Pikachu input image.
3. Inspect the saved image statistics to determine whether the output is black.

## Observed behavior

- Reproduction could not be completed: OutOfMemoryError: CUDA out of memory. Tried to allocate 130.00 MiB. GPU 0 has a total capacity of 94.96 GiB of which 59.69 MiB is free. Process 502587 has 1.78 GiB memory in use. Process 745081 has 86.44 GiB memory in use. Including non-PyTorch memory, this process has 6.62 GiB memory in use. Of the allocated memory 5.97 GiB is allocated by PyTorch, and 116.33 MiB is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reproduction environment failed before the QwenImageEditPipeline call finished.
