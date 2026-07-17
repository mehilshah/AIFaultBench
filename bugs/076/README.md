# Mask R-CNN HDF5 load_weights repro

This folder reproduces the weight-loading failure reported in Mask R-CNN issue 3050.

What it does:
- Uses the repo's `MaskRCNN.load_weights()` implementation from `codebase/mrcnn/model.py`.
- Builds a tiny standalone `keras` model whose weights are `keras.src.backend.Variable`.
- Writes a legacy-style `.h5` file with a matching `conv1` layer.
- Calls `load_weights(..., by_name=True)` and triggers the same `NotImplementedError`.

Run it:
```bash
bash setup_env.sh
bash run_repro.sh
```

Expected result:
- `MaskRCNN.load_weights()` raises `NotImplementedError`
- The error says HDF5 loading is not supported for non-`tf.Variable` weights and suggests `save_format='tf'`
