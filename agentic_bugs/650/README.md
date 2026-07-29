# Bug 650

At the pinned smolagents commit, `GradioUI.create_app()` passes `theme="ocean"` to `gr.Blocks`. Gradio 6.0.1 no longer accepts that keyword, so the UI cannot be created and raises the reported `TypeError`. The offline repro uses a metadata-only stub agent and checks the exact exception; it reproduced on this host.

Files: `repro.py` is the minimal reproducer, `requirements.txt` pins Gradio, `setup_env.sh` creates the environment, `run_repro.sh` runs it, and the two log files contain the final captured result. `reproduction.json` and `reproduction_trajectory.md` record the evidence.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
