# Reproduction Trajectory — Bug 674: dspy

- **Bug report:** [https://github.com/stanfordnlp/dspy/issues/9589](https://github.com/stanfordnlp/dspy/issues/9589)
- **Repository:** stanfordnlp/dspy @ `9cdb0aac28b2a04b064e40697ccd301872cf6a43`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the pinned commit.
2. Created an isolated virtual environment and installed the exact pinned runtime dependencies plus the checkout.
3. Saved a two-predictor program with a sentinel demo on each predictor, deleted the `b.predict` JSON entry, and loaded that state into a fresh program without making any LLM calls.

## Observed behavior

- The loader raised `KeyError: 'b.predict'`, but the fresh program's `a.predict.demos` had already changed from `[]` to the saved sentinel demo.
- `run_repro.sh` printed `OBSERVED BUG: KeyError('b.predict') left a.predict.demos partially loaded` and exited with status 1, as intended for the detected faulty behavior.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
