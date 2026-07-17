# Bug 476

The reported failure is reproducible with `torch-geometric==2.6.1`.

Reproduction flow:
1. Run `bash setup_env.sh`
1. Run `bash run_repro.sh`
1. Inspect `repro_stdout.log` and `repro_stderr.log`

Observed result:
- `torch_geometric.__version__` is `2.6.1`
- `hasattr(torch_geometric, "HashTensor")` is `False`
- `from torch_geometric import HashTensor` raises `ImportError`

Relevant inputs:
- issue URL: `https://github.com/pyg-team/pytorch_geometric/issues/10116`
- local repo checkout: `codebase/`
- broken package version: `torch-geometric==2.6.1`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
