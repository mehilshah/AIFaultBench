# Bug 150

Reproduction bundle for Hugging Face Transformers issue 42502.

## Bug Summary

`DataCollatorWithFlattening` concatenates `sample["labels"]` as if it were always a Python list. When `labels` are provided as `torch.Tensor`, the collator raises:

`TypeError: can only concatenate list (not "Tensor") to list`

## How to Reproduce

```bash
bash run_repro.sh
```

The run writes:

- `repro_stdout.log`
- `repro_stderr.log`
- `reproduction.json`

## Notes

- The repro uses the local `codebase/src` tree.
- Runtime dependencies are declared in `requirements.txt`.
