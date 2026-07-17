# Bug 411 Repro

This folder reproduces the PEFT `modules_to_save` failure from issue 602.

## What fails

`AutoModelForSequenceClassification.from_pretrained(..., device_map="auto")` on `bigscience/bloomz-560m` with an offload budget triggers `accelerate` offload hooks after PEFT wraps `score` in `ModulesToSaveWrapper`.

The control case without `device_map="auto"` routes gradients to `modules_to_save.default`.

## Run

```bash
bash run_repro.sh
```

The run writes:

- `repro_stdout.log`
- `repro_stderr.log`

The repro exits non-zero when the bug is observed.
