# Reproduction Trajectory — Bug 313: pytorch_geometric

- **Bug report:** [https://github.com/pyg-team/pytorch_geometric/issues/10548](https://github.com/pyg-team/pytorch_geometric/issues/10548)
- **Repository:** pyg-team/pytorch_geometric @ `44dee49ad88cf5253e8092cfce3e453c00bc8c3e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Downloaded the issue attachments into `batch_edge_index.txt` and `batch_edge_attr.txt`.
2. Created a CUDA-capable Python environment and installed `torch==2.8.0+cu128`, `torch_cluster==1.6.3+pt28cu128`, `numpy==2.5.1`, and `scipy==1.18.0`.
3. Ran `repro.py`, which first verified the CPU path and then invoked `graclus_cluster` on GPU.
4. Observed that the GPU invocation timed out after printing the start banner.

## Observed behavior

- repro_stdout.log shows the CPU path completed: `cpu_done shape=(64,) first10=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
- repro_stdout.log shows the GPU path reached `gpu_start shape=(4096,) device=cuda:0` and then stopped producing output.
- repro_exitcode.txt contains `124`, which is the `timeout` exit code from `run_repro.sh`.
- The exact reported `torch==2.4.1+cu124` wheel cannot execute on this workspace's sm_120 GPU, so the repro uses a compatible cu128 stack to exercise the same native `graclus_cluster` code path.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
