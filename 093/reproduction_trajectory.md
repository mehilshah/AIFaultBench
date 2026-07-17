# Reproduction Trajectory — Bug 093: x-transformers

- **Bug report:** [https://github.com/lucidrains/x-transformers/issues/228](https://github.com/lucidrains/x-transformers/issues/228)
- **Repository:** lucidrains/x-transformers @ `aa380f17b6f1e762604278ad2cd9b6ecc804f35e`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a local virtualenv and install the dependencies from requirements.txt.
2. Run repro.py via ./run_repro.sh, which instantiates TransformerWrapper with Decoder(attn_num_mem_kv=20, attn_one_kv_head=True) and feeds an 8x1024 token batch.

## Observed behavior

- With the restored local codebase, ./run_repro.sh completes successfully and prints torch.Size([8, 1024]) torch.int64 followed by torch.Size([8, 1024, 32]) torch.float32. No tensor-size mismatch is raised.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The current local checkout does not trigger the reported failure; the model forward pass succeeds.
