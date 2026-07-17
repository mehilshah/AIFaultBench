# Bug 437 Repro

Issue: [huggingface/accelerate#1419](https://github.com/huggingface/accelerate/issues/1419)

This bundle reproduces the W&B logging symptom from the report using the pinned `accelerate` checkout in `codebase/`.

What happens:
- `batch_train_loss` logs cleanly.
- `batch_eval_loss` is logged with a separate counter that goes backwards relative to W&B's current step.
- W&B drops the out-of-order evaluation entries and reports the drop in its offline log output.

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```

Generated output:
- `repro_stdout.log`
- `repro_stderr.log`

