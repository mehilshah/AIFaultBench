# Reproduction Trajectory — Bug 379: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1598](https://github.com/huggingface/accelerate/issues/1598)
- **Repository:** huggingface/accelerate @ `e60a4243988a636bda8a6bf99044fb313d5a9e0e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny nn.Module with Embedding and Linear layers.
2. Start a multiprocessing.Process with the spawn start method using the undecorated model; the child starts successfully.
3. Run accelerate.big_modeling.dispatch_model(model, {"": "cpu"}) and pass the wrapped model to multiprocessing.Process; p.start() raises PicklingError.

## Observed behavior

- A baseline TinyModel process starts successfully under spawn, but after dispatch_model(model, {"": "cpu"}) the parent fails during p.start() with _pickle.PicklingError: Can't pickle <function Embedding.forward ...>: it's not the same object as torch.nn.modules.sparse.Embedding.forward.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
