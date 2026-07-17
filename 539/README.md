# Bug 539

This folder is a self-contained repro bundle for Pyro issue 3032.

Observed behavior:
- Torch 1.9.0 does not accept the `indexing=` keyword on `torch.meshgrid`.
- The historical CI failure came from code that called `torch.meshgrid(xs, ys, indexing="xy")`.
- The checked-out `codebase/examples/neutra.py` already contains the workaround, so the repo copy itself is fixed.

How to reproduce:
- `bash run_repro.sh`

Captured evidence:
- `repro_stdout.log`
- `repro_stderr.log`

Environment notes:
- Python 3.9 is used for the repro environment.
- The pinned dependency is `torch==1.9.0+cpu`.
