# Bug 056

Reproduction bundle for keras-io issue [#1672](https://github.com/keras-team/keras-io/issues/1672).

## What fails

The Vision Transformer example builds a resized image tensor from `ops.convert_to_tensor([image])` and then passes it into `Patches`. With `keras==3.0.0` and `tensorflow-cpu==2.16.1`, that path raises:

```text
InvalidArgumentError: ... cannot compute Conv2D as input #1 ... was expected to be a int32 tensor but is a float tensor
```

## Files

- `repro.py` - minimal failing script
- `requirements.txt` - pinned reproducing dependencies
- `setup_env.sh` - creates the isolated Python environment
- `run_repro.sh` - runs the repro inside that environment
- `manifest.json` - bundle metadata

## Run locally

```bash
bash setup_env.sh
bash run_repro.sh
```

