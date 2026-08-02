# Reproduction Trajectory — Bug 650: smolagents

- **Bug report:** [https://github.com/huggingface/smolagents/issues/1887](https://github.com/huggingface/smolagents/issues/1887)
- **Repository:** huggingface/smolagents @ `2ae00fb092d1b0e7d74de06e738dd48d04a8b2c2`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read the report, which specifies the incompatible Gradio version (`6.0.1`) and identifies `GradioUI.create_app()` as the failing path.
2. Ran `bash setup_codebase.sh`, which cloned `huggingface/smolagents` and checked out commit `2ae00fb092d1b0e7d74de06e738dd48d04a8b2c2`.
3. Created `.venv`, installed `gradio==6.0.1`, and installed the pinned checkout editable.
4. Ran `repro.py` through `bash run_repro.sh`. The script constructs `GradioUI` with a metadata-only stub agent and calls `create_app()`, so no model or provider request is made.

## Observed behavior

- The final run printed `OBSERVED BUG: TypeError: BlockContext.__init__() got an unexpected keyword argument 'theme'` and exited with status 1.
- The traceback reaches `codebase/src/smolagents/gradio_ui.py:419`, at `gr.Blocks(theme="ocean", fill_height=True)`.
- The final environment used `gradio=6.0.1` and `smolagents=1.24.0.dev0` from the pinned checkout.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
