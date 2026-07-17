# Bug 078 Reproduction Bundle

This folder reproduces the nested-tensor backward failure reported in
`bug_report.txt` for `vit_pytorch.na_vit_nested_tensor_3d.NaViT`.

## What fails

Forward pass succeeds, but `loss.backward()` raises:

`RuntimeError: Function UnbindBackwardAutogradNestedTensor0 returned an invalid gradient ...`

The failure comes from the 3D nested-tensor path in
`codebase/vit_pytorch/na_vit_nested_tensor_3d.py`, at the final
`pooled.unbind()` call.

## Reproduction

1. Create the virtual environment and install dependencies:
   `bash setup_env.sh`
2. Run the reproducer:
   `bash run_repro.sh`

The script writes:

- `repro_stdout.log`
- `repro_stderr.log`

## Expected result

The reproducer is expected to fail during backward with the nested-tensor
gradient shape mismatch described in the bug report.
