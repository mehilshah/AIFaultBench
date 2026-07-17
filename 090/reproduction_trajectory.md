# Reproduction Trajectory — Bug 090: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/273](https://github.com/lucidrains/x-transformers/issues/273)
- **Repository:** lucidrains/x-transformers @ `43960ad12ac2eb3c943688430ec58fa8e82752e7`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a minimal XTransformer with encoder and decoder stacks from the local codebase.
2. Ran one forward/backward pass on random src and tgt tensors.
3. Checked model.encoder.to_logits.weight.grad and confirmed it remained None.

## Observed behavior

- repro.py prints encoder.to_logits.weight.requires_grad=True and encoder.to_logits.weight.grad_is_none=True after a forward/backward pass.
- repro_stdout.log contains: REPRODUCED: encoder.to_logits.weight is unused in the forward pass.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```
