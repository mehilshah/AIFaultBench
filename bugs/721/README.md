# Bug 721

At the pinned `browser-use` 0.12.1 checkout, CodeAgent accepts an unstarted
`Browser` but does not initialize its root CDP client. The deterministic repro
uses a recorded in-process ChatBrowserUse reply, verifies the missing
`BrowserStateRequestEvent` result, and then verifies the exact
`AssertionError: Root CDP client not initialized` recorded for `evaluate()`.
It reproduced on this host without a browser process, external website, LLM
provider, API key, or telemetry request.

Files: `repro.py` is the reproduction, `requirements.txt` contains the pinned
runtime dependencies, `setup_env.sh` creates the isolated environment,
`run_repro.sh` runs it, and the stdout/stderr logs plus JSON and trajectory
files capture the observed result.

Run after cloning the pinned checkout:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
