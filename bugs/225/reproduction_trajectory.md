# Reproduction Trajectory — Bug 225: Crawl4AI

- **Bug report:** [https://github.com/unclecode/crawl4ai/issues/1442](https://github.com/unclecode/crawl4ai/issues/1442)
- **Repository:** unclecode/crawl4ai @ `4e1c4bd`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a tiny FastAPI app that uses get_token_dependency({"security": {"jwt_enabled": True}}) exactly as the server does.
2. Send one request without an Authorization header, one with an invalid bearer token, and one with a valid token created by create_access_token().
3. Observe that the missing-token request is accepted with HTTP 200 instead of HTTP 401.

## Observed behavior

- Reproduction succeeded. In the local FastAPI harness that reuses codebase/deploy/docker/auth.py, a request without Authorization returned 200 with {"success": true, "dependency_value": null}, while an invalid bearer token returned 401 and a valid token returned 200. This matches the bug report and the code path at codebase/deploy/docker/auth.py:31-35 together with the protected route pattern in codebase/deploy/docker/server.py:431-435.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
