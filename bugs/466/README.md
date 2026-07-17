# Bug 466

This folder contains a minimal repro bundle for Lightning issue `#21576`.

Observed result:
- The issue report is a request to stop mentioning `@Blaizzy`.
- In the checked-out Lightning commit, there is no local `@Blaizzy` reference to reproduce.
- The repo does still mention `@ethanwharris`, but that is unrelated to the reported user.

Files generated here:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Run locally with:
`bash run_repro.sh`
