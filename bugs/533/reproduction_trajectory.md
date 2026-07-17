# Reproduction Trajectory — Bug 533: pytorch-lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21513](https://github.com/Lightning-AI/pytorch-lightning/issues/21513)
- **Repository:** Lightning-AI/pytorch-lightning @ `0a0f0610a4d223a258cd73e65abe852a8f703226`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the local .venv with ./setup_env.sh.
2. Run ./run_repro.sh, which sets PYTHONPATH to codebase/src and executes repro.py.
3. Observe trainer.fit() fail during the compiled training_step path at toggle_optimizer().

## Observed behavior

- Running ./run_repro.sh fails on the first training step. The captured stderr ends in torch._dynamo.utils.tuple_iterator_getitem with IndexError: tuple index out of range while executing LightningModule.toggle_optimizer() from a torch.compile()d model.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
