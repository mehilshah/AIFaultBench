# Reproduction Trajectory — Bug 145: sentence-transformers

- **Bug report:** [https://github.com/huggingface/sentence-transformers/issues/3175](https://github.com/huggingface/sentence-transformers/issues/3175)
- **Repository:** huggingface/sentence-transformers
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run bash setup_env.sh to create the local virtual environment and install the pinned repro dependencies.
2. Run bash run_repro.sh from the bug folder.
3. Observe the printed similarity value tensor([[0.5375]]).

## Observed behavior

- Running the exact StaticEmbedding.from_distillation example in this folder prints similarity tensor([[0.5375]]) instead of the docstring's tensor([[0.9177]]).

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
