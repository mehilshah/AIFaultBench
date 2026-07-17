# Reproduction Trajectory — Bug 140: safetensors

- **Bug report:** [https://github.com/huggingface/safetensors/issues/439](https://github.com/huggingface/safetensors/issues/439)
- **Repository:** huggingface/safetensors @ `08db340`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a 10x10 tensor and save it with safetensors.torch.save_file.
2. Open the file with safe_open(..., framework='pt', device='cpu').
3. Call get_slice('test')[0, :] to exercise integer indexing on the lazy slice object.

## Observed behavior

- save_file succeeded and the failure happens at safe_open(...).get_slice('test')[0, :].
- Observed exception: TypeError: argument 'slices': failed to extract enum Slice ('Slice | Slices')
- variant Slice (Slice): TypeError: failed to extract field Slice::Slice.0, caused by TypeError: 'tuple' object cannot be converted to 'PySlice'
- variant Slices (Slices): TypeError: failed to extract field Slice::Slices.0, caused by TypeError: 'int' object cannot be converted to 'PySlice'
- The traceback matches the reported failure: argument 'slices' cannot extract an int as PySlice.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
