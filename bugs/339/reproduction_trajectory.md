# Reproduction Trajectory — Bug 339: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/3227](https://github.com/facebookresearch/detectron2/issues/3227)
- **Repository:** facebookresearch/detectron2 @ `bb44e10a93d3c136760d6d31d387f600429e1c61`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a config with DATASETS.TEST=('dummy_dataset',), DATASETS.PROPOSAL_FILES_TEST=('dummy.pkl',), and MODEL.LOAD_PROPOSALS=True.
2. Register a dummy dataset name so the loader path matches the reported eval-only setup.
3. Call build_detection_test_loader(cfg, cfg.DATASETS.TEST[0]).
4. Observe ValueError because _test_loader_from_config converts the string name to ['dummy_dataset'] and then uses that list as the argument to list(cfg.DATASETS.TEST).index(...).

## Observed behavior

- In the distilled local Detectron2 package under codebase/, build_detection_test_loader(cfg, cfg.DATASETS.TEST[0]) raises ValueError: ['dummy_dataset'] is not in list from detectron2/data/build.py:_test_loader_from_config.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
