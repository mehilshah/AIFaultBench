# Reproduction Trajectory — Bug 523: accelerate

- **Bug report:** [https://github.com/huggingface/accelerate/issues/1174](https://github.com/huggingface/accelerate/issues/1174)
- **Repository:** huggingface/accelerate @ `2f83b1afefae2c13f9be36419da9f39c283de07d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a torch.nn.Linear model and SGD optimizer.
2. Instantiate accelerate.Accelerator(cpu=True).
3. Call accelerator.prepare(optimizer).

## Observed behavior

- Running Accelerator(cpu=True).prepare(optimizer) raises AssertionError in accelerate/src/accelerate/state.py:544 when AcceleratorState() inside AcceleratedOptimizer.__init__ reinitializes PartialState with cpu=False. stderr tail: AssertionError: The current device and desired device are not the same. If the `PartialState` was generated before the `Accelerator` has been instantiated, ensure the `cpu` flag is the same for both. In this case, the `PartialState` has True and the desired device is False. Please use `cpu=True`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
