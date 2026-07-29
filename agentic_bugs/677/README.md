# Bug 677

Semantic Kernel 1.37.0 assumes every non-`AsyncStream` chat response has a
`usage` attribute. OpenTelemetry's real streaming `StreamWrapper` does not, so
a traced streaming request crashes before the stream is consumed. The offline
repro uses that wrapper and a fake OpenAI client; it currently reproduces the
reported `AttributeError` on this host.

Files: `repro.py` is the minimal reproduction, `requirements.txt` pins its
dependencies, `setup_env.sh` creates the environment, `run_repro.sh` runs it,
and the log/JSON/trajectory files record the observed result.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
