# Reproduction Bundle

Issue: `encoder.to_logits.weight` exists on the encoder side of `XTransformer`, but it is not used by the forward pass.

## Run

```bash
./setup_env.sh
./run_repro.sh
```

## What the repro checks

`repro.py` builds a minimal `XTransformer`, runs a forward/backward pass, and prints whether `encoder.to_logits.weight.grad` stays `None`.
