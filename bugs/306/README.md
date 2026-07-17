# Bug 306 Reproduction

This folder reproduces the `AttentionPool2d` / `RotAttentionPool2d` `num_classes=0` bug described in issue 2682.

## What it shows

- `timm.create_model("resnet50_clip.openai", pretrained=True, num_classes=0, global_pool="")` produces different outputs across two instantiations.
- `timm.create_model("resnet50_clip.openai", pretrained=True)` followed by `reset_classifier(0, "")` is stable and produces identical outputs.

## Repro command

```bash
bash run_repro.sh
```

## Observed result

- Buggy path max diff: non-zero
- Workaround max diff: `0.0`

The run writes the schema result to `reproduction.json` and captures stdout/stderr in:

- `repro_stdout.log`
- `repro_stderr.log`
