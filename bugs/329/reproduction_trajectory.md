# Reproduction Trajectory — Bug 329: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10505](https://github.com/pyg-team/pytorch_geometric/issues/10505)
- **Repository:** pyg-team/pytorch_geometric @ `76ff9c2ce18c8cebf52122b57e2aeadce9793d10`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a fresh Python 3.12 virtualenv.
2. Install the dependencies from `requirements.txt` using the CPU PyTorch index.
3. Run `PYTHONPATH=codebase python repro.py`.

## Observed behavior

- Running `torch.jit.script(HGTConv(16, 16, ([], [])))` in a clean venv with torch 2.8.0+cpu and the local codebase raises `TypeError: 'set' object in attribute 'ParameterDict.CLASS_ATTRS' is not a valid constant.`

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
