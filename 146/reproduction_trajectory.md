# Reproduction Trajectory — Bug 146: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3262](https://github.com/huggingface/sentence-transformers/issues/3262)
- **Repository:** huggingface/sentence-transformers @ `8e18e27`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Installed dependencies into a local virtual environment with bash setup_env.sh.
2. Ran bash run_repro.sh against the vendored codebase and a whitespace-sensitive GPT-2 tokenizer model.
3. Observed that encode() collapses ' test' and 'test' to the same embedding while the tokenizer does not.

## Observed behavior

- With the local sentence-transformers source, model.tokenizer('test').input_ids=[9288] and model.tokenizer(' test').input_ids=[1332], so the tokenizer distinguishes leading whitespace. However, model.encode('test', normalize_embeddings=True) and model.encode(' test', normalize_embeddings=True) both returned the same 2D embedding [0.7071067690849304, -0.7071067690849304], with max_abs_diff=0.0.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
