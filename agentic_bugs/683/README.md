# Bug 683

mem0's Qdrant store forwards `host`, `port`, and `api_key` without an `https`
setting. With qdrant-client 1.13.3, that selects HTTPS even when the Qdrant
endpoint is plain HTTP. The reproduction starts a local plain-HTTP endpoint and
checks that constructing mem0's Qdrant store raises the reported TLS protocol
error. On this host, the bug reproduces.

Files: `repro.py` is the deterministic reproducer; `requirements.txt` pins its
dependencies; `setup_env.sh` installs them; `run_repro.sh` is the entrypoint;
`repro_stdout.log` and `repro_stderr.log` are final-run evidence;
`reproduction.json` and `reproduction_trajectory.md` record the outcome.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
