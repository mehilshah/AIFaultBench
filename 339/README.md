# Bug 339 Repro

This folder reproduces the Detectron2 bug from issue 3227 with a distilled local
package that preserves the failing control flow.

## What fails

`detectron2/data/build.py::_test_loader_from_config` turns a string dataset name into a one-item list and then uses that list as the argument to `list(cfg.DATASETS.TEST).index(...)`.

The repro reaches:

`ValueError: ['dummy_dataset'] is not in list`

## How to run

1. `bash setup_env.sh`
2. `bash run_repro.sh`

The launcher writes:

* `repro_stdout.log`
* `repro_stderr.log`

## Repro summary

The script uses:

* `cfg.DATASETS.TEST = ('dummy_dataset',)`
* `cfg.DATASETS.PROPOSAL_FILES_TEST = ('dummy.pkl',)`
* `cfg.MODEL.LOAD_PROPOSALS = True`

Then it calls:

`build_detection_test_loader(cfg, cfg.DATASETS.TEST[0])`

which raises `ValueError: ['dummy_dataset'] is not in list`.
