# Reproduction Trajectory — Bug 273: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/2627](https://github.com/huggingface/peft/issues/2627)
- **Repository:** huggingface/peft @ `2bc97c02b777f17b371510f2fa4d672519664198`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load hf-internal-testing/tiny-random-Gemma3ForCausalLM with attn_implementation='eager'.
2. Wrap the model with VBLoRA using the same Gemma 3 target-module path as the reported issue.
3. Switch the model to train mode so the VBLoRA logits check is active.
4. Call generate() with cache_implementation='static' and a compile config that enables torch.compile on this CPU-only repro.

## Observed behavior

- Data-dependent branching
  Explanation: Detected data-dependent branching (e.g. `if my_tensor.sum() > 0:`). Dynamo does not support tracing dynamic control flow.
  Hint: This graph break is fundamental - it is unlikely that Dynamo will ever be able to trace through your code. Consider finding a workaround.
  Hint: Use `torch.cond` to express dynamic control flow.

  Developer debug context: attempted to jump with TensorVariable()


from user code:
   File ".venv_test/lib/python3.12/site-packages/transformers/utils/generic.py", line 961, in wrapper
    output = func(self, *args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/transformers/models/gemma3/modeling_gemma3.py", line 658, in forward
    outputs: BaseModelOutputWithPast = self.model(
  File ".venv_test/lib/python3.12/site-packages/transformers/utils/generic.py", line 1069, in wrapper
    outputs = func(self, *args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/transformers/models/gemma3/modeling_gemma3.py", line 559, in forward
    layer_outputs = decoder_layer(
  File ".venv_test/lib/python3.12/site-packages/transformers/modeling_layers.py", line 94, in __call__
    return super().__call__(*args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1751, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1762, in _call_impl
    return forward_call(*args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/transformers/utils/deprecation.py", line 172, in wrapped_func
    return func(*args, **kwargs)
  File ".venv_test/lib/python3.12/site-packages/transformers/models/gemma3/modeling_gemma3.py", line 393, in forward
    hidden_states, self_attn_weights = self.self_attn(
  File ".venv_test/lib/python3.12/site-packages/transformers/models/gemma3/modeling_gemma3.py", line 319, in forward
    query_states = self.q_proj(hidden_states).view(hidden_shape).transpose(1, 2)
  File "codebase/src/peft/tuners/vblora/layer.py", line 244, in forward
    A, B = self._get_lora_matrices(active_adapter)
  File "codebase/src/peft/tuners/vblora/layer.py", line 191, in _get_lora_matrices
    if self.training and vblora_logits_A[0, 0].isinf().any():

Set TORCHDYNAMO_VERBOSE=1 for the internal stack trace (please do this especially if you're reporting a bug to PyTorch). For even more developer context, set TORCH_LOGS="+dynamo"

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
