# Bug 038 Reproduction Bundle

This folder reproduces the RoPE shape-mismatch bug reported in:
`https://github.com/labmlai/annotated_deep_learning_paper_implementations/issues/244`

## What fails

`codebase/labml_nn/transformers/rope/__init__.py` builds cached cosine and sine tensors with a last dimension of `4`, but the RoPE path applies them to a sliced tensor with a last dimension of `3` when `RotaryPositionalEmbeddings(3)` is used.

The observed runtime error is:

`RuntimeError: The size of tensor a (3) must match the size of tensor b (4) at non-singleton dimension 3`

## How to run

```bash
bash run_repro.sh
```

`setup_env.sh` creates a local virtual environment and installs the minimal runtime dependencies.
