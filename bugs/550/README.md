# Bug 550 Repro Bundle

This folder contains a minimal reproduction for TorchRL issue 3288.

What fails:

- `MultiAgentNetBase` ignores `agent_dim` in the `share_params=True` branch.
- The final validation always checks `output.shape[-2]`, which is wrong when the agent axis is not the penultimate axis of the output tensor.

Observed result in this bundle:

- `agent_dim=1` and `agent_dim=0` both fail with the same `ValueError`.
- The error reports `shape[-2]=3` while the actual output shape is `torch.Size([4, 3, 6, 4])`.

How to run:

1. `bash setup_env.sh`
2. `bash run_repro.sh`

Notes:

- The bundle uses the local `codebase/` directly through `PYTHONPATH`.
- The environment bootstrap installs a CPU-only Torch wheel to avoid the broken system Torch install in this container.
