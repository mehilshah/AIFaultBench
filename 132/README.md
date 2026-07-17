# Flair TextPairRegressor repro

This folder reproduces the `TextPairRegressor` state-dict loading failure reported in flair issue 3536.

What happens:

```python
model._init_model_with_state_dict(model._get_state_dict())
```

raises:

```text
TypeError: TextPairRegressor.__init__() got an unexpected keyword argument 'document_embeddings'
```

## Repro steps

1. Run `bash run_repro.sh`
2. Inspect `repro_stdout.log` and `repro_stderr.log`

The repro uses a small `DocumentTFIDFEmbeddings` instance so it does not need any model downloads.
