# Reproduction Trajectory — Bug 317: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21757](https://github.com/Lightning-AI/pytorch-lightning/issues/21757)
- **Repository:** Lightning-AI/pytorch-lightning @ `35e56ef93582c60c8ec5ca2bf1025e7c414d6bb6`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install torch 2.6.0+cpu and the Lightning runtime deps in an isolated venv.
2. Fit a simple LightningModule that stores a custom nn.Module in hyperparameters and save a checkpoint.
3. Verify the checkpoint loads with `torch.load(..., weights_only=False)`.
4. Call `Tuner(trainer).lr_find(...)` on a fresh trainer and observe the restore-time UnpicklingError.

## Observed behavior

- Manual checkpoint load with weights_only=False succeeded: ['callbacks', 'epoch', 'global_step', 'hparams_name', 'hyper_parameters']
lr_find raised UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, [1mdo those steps only if you trust the source of the checkpoint[0m. 
	(1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
	(2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
	WeightsUnpickler error: Unsupported global: GLOBAL __main__.TorchCoder was not an allowed global by default. Please use `torch.serialization.add_safe_globals([TorchCoder])` or the `torch.serialization.safe_globals([TorchCoder])` context manager to allowlist this global if you trust this class/function.

Check the documentation of torch.load to learn more about types accepted by default with weights_only https://pytorch.org/docs/stable/generated/torch.load.html.
Traceback (most recent call last):
  File "repro.py", line 98, in main
    Tuner(trainer2).lr_find(
  File "codebase/src/lightning/pytorch/tuner/tuning.py", line 191, in lr_find
    self._trainer.fit(model, train_dataloaders, val_dataloaders, datamodule)
  File "codebase/src/lightning/pytorch/trainer/trainer.py", line 590, in fit
    call._call_and_handle_interrupt(
  File "codebase/src/lightning/pytorch/trainer/call.py", line 49, in _call_and_handle_interrupt
    return trainer_fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/lightning/pytorch/trainer/trainer.py", line 636, in _fit_impl
    self._run(model, ckpt_path=ckpt_path, weights_only=weights_only)
  File "codebase/src/lightning/pytorch/trainer/trainer.py", line 1063, in _run
    call._call_callback_hooks(self, "on_fit_start")
  File "codebase/src/lightning/pytorch/trainer/call.py", line 228, in _call_callback_hooks
    fn(trainer, trainer.lightning_module, *args, **kwargs)
  File "codebase/src/lightning/pytorch/callbacks/lr_finder.py", line 130, in on_fit_start
    self.lr_find(trainer, pl_module)
  File "codebase/src/lightning/pytorch/callbacks/lr_finder.py", line 113, in lr_find
    self.optimal_lr = _lr_find(
                      ^^^^^^^^^
  File "codebase/src/lightning/pytorch/tuner/lr_finder.py", line 288, in _lr_find
    trainer._checkpoint_connector.restore(ckpt_path)
  File "codebase/src/lightning/pytorch/trainer/connectors/checkpoint_connector.py", line 247, in restore
    self.resume_start(checkpoint_path, weights_only=weights_only)
  File "codebase/src/lightning/pytorch/trainer/connectors/checkpoint_connector.py", line 83, in resume_start
    loaded_checkpoint = self.trainer.strategy.load_checkpoint(checkpoint_path, weights_only=weights_only)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/lightning/pytorch/strategies/strategy.py", line 368, in load_checkpoint
    return self.checkpoint_io.load_checkpoint(checkpoint_path, weights_only=weights_only)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/lightning/fabric/plugins/io/torch_io.py", line 91, in load_checkpoint
    return pl_load(path, map_location=map_location, weights_only=weights_only)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/lightning/fabric/utilities/cloud_io.py", line 73, in _load
    return torch.load(
           ^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/torch/serialization.py", line 1470, in load
    raise pickle.UnpicklingError(_get_wo_message(str(e))) from None
_pickle.UnpicklingError: Weights only load failed. This file can still be loaded, to do so you have two options, [1mdo those steps only if you trust the source of the checkpoint[0m. 
	(1) In PyTorch 2.6, we changed the default value of the `weights_only` argument in `torch.load` from `False` to `True`. Re-running `torch.load` with `weights_only` set to `False` will likely succeed, but it can result in arbitrary code execution. Do it only if you got the file from a trusted source.
	(2) Alternatively, to load with `weights_only=True` please check the recommended steps in the following error message.
	WeightsUnpickler error: Unsupported global: GLOBAL __main__.TorchCoder was not an allowed global by default. Please use `torch.serialization.add_safe_globals([TorchCoder])` or the `torch.serialization.safe_globals([TorchCoder])` context manager to allowlist this global if you trust this class/function.

Check the documentation of torch.load to learn more about types accepted by default with weights_only https://pytorch.org/docs/stable/generated/torch.load.html.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
