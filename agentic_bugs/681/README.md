# Bug 681

This bundle reproduces mem0 CLI issue 5931: explicit JSON `null` values for
memory fields reach unsafe slicing and `len()` calls in its output formatters.
`repro.py` invokes both affected formatters entirely locally and checks for
their reported `TypeError` failures. On this host, the pinned buggy checkout
reproduces the fault.

Files:

- `repro.py` — deterministic local reproduction.
- `requirements.txt` — pinned runtime dependency.
- `setup_env.sh` / `run_repro.sh` — environment setup and entrypoint.
- `repro_stdout.log` / `repro_stderr.log` — final captured run output.
- `reproduction.json` / `reproduction_trajectory.md` — evidence and narrative.

Run:

```bash
bash setup_codebase.sh
bash run_repro.sh
```
