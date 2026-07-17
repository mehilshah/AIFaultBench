# DeepSeek V2 aux hidden-state repro bundle

This folder contains a self-contained repro harness for the bug report about
`vllm/model_executor/models/deepseek_v2.py` missing the final layer's auxiliary
hidden state.

What the harness does:

1. Reads the checked-in DeepSeek V2 source.
2. Confirms the final-layer capture branch is already present.
3. Simulates the pre-fix and current behavior for a 1-layer model where the
   auxiliary hidden state is requested at the last layer.

Result in this tree:

- `reproducible`: `false`
- `blocking_reason`: the code already includes the post-loop `end_layer`
  capture, so the reported bug is not present here.

Run it with:

```bash
bash run_repro.sh
```
