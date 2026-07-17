# Bug 478

This folder reproduces the Florence2 training-loss double-shift bug reported in
`https://github.com/huggingface/transformers/issues/46897`.

What the repro does:
- builds a tiny random `Florence2ForConditionalGeneration` model from the local `codebase/`
- runs a forward pass with synthetic labels
- compares the model loss to:
  - the correct `CrossEntropyLoss` on the provided labels
  - the shifted-label loss that `ForCausalLMLoss` computes internally

Observed result:
- the model loss matches the shifted-label loss
- the model loss does not match the direct cross-entropy on the provided labels

Files:
- `repro.py` runs the reproduction and writes `reproduction.json`
- `requirements.txt` lists the minimal Python dependencies
- `setup_env.sh` creates a local virtualenv and installs the runtime deps
- `run_repro.sh` executes the repro and captures stdout/stderr

Run:
```bash
bash setup_env.sh
bash run_repro.sh
```

