# Reproduction Trajectory — Bug 078: vit-pytorch

- **Bug report:** [https://github.com/lucidrains/vit-pytorch/issues/332](https://github.com/lucidrains/vit-pytorch/issues/332)
- **Repository:** lucidrains/vit-pytorch @ `141239ca86afc6e1fe6f4e50b60d173e21ca38ec`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install torch 2.4.0 and the lightweight dependencies from requirements.txt.
2. Run repro.py, which loads vit_pytorch/na_vit_nested_tensor_3d.py directly from the local codebase.
3. Observe that the forward pass completes, then loss.backward() raises the nested-tensor UnbindBackwardAutogradNestedTensor0 gradient-shape error.

## Observed behavior

- Using torch 2.4.0, forward succeeds on a small NaViT 3D nested-tensor input, but backward fails with RuntimeError: Function UnbindBackwardAutogradNestedTensor0 returned an invalid gradient at index 0 ... expected shape compatible with [2, j2, 16]. The failing operation is the final pooled.unbind() path in codebase/vit_pytorch/na_vit_nested_tensor_3d.py.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
