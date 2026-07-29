# Reproduction Trajectory — Bug 683: mem0

- **Bug report:** [https://github.com/mem0ai/mem0/issues/5378](https://github.com/mem0ai/mem0/issues/5378)
- **Repository:** mem0ai/mem0 @ `90f2d24e832302c97e0daa55454b29657e742c15`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`; its initial clone was incomplete, so fetched the pinned commit from its already-configured upstream remote and checked it out. Verified `HEAD` was `90f2d24e832302c97e0daa55454b29657e742c15`.
2. Ran `bash setup_env.sh` to create `.venv`, install pinned qdrant-client 1.13.3 and mem0 runtime dependencies, and install the checkout editable.
3. Ran `bash run_repro.sh`. The repro starts a standard-library plain-HTTP server bound only to localhost, then constructs mem0's `Qdrant` store with `host`, `port`, and `api_key`.

## Observed behavior

- The final run exited with status 1 and printed: `BUG REPRODUCED: host+port+api_key attempted HTTPS against plain HTTP: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1000)`.
- The local HTTP endpoint received a TLS connection attempt because the pinned mem0 Qdrant constructor forwards `host`, `port`, and `api_key` without an `https=False` option.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
