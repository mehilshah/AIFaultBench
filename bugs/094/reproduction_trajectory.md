# Reproduction Trajectory — Bug 094: PaLM-rlhf-pytorch

- **Bug report:** [https://github.com/lucidrains/PaLM-rlhf-pytorch/issues/46](https://github.com/lucidrains/PaLM-rlhf-pytorch/issues/46)
- **Repository:** lucidrains/PaLM-rlhf-pytorch @ `e624afd8860d6df8f7a429dbe518a2fd40b4cc34`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Create a virtual environment and install the repro dependencies from requirements.txt.
2. Run bash run_repro.sh against the local codebase checkout.
3. Inspect the printed gradient lists for missing norm.gamma parameters.

## Observed behavior

- Plain backward on a tiny PaLM instance reported plain_backward_missing=[] and produced nonzero gradients for layers.0.fn.norm.gamma (grad_sum=0.05676254257559776), layers.1.fn.norm.gamma (grad_sum=0.03758058324456215), and norm.gamma (grad_sum=0.03201062232255936).
- CPU DistributedDataParallel with world_size=1 reported ddp_backward_missing=[] and completed backward without error.
- The direct missing-parameter check in the local checkout returned an empty list.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The local checkout does not exhibit the reported unused-parameter behavior; norm.gamma receives gradients in both plain and DDP-backed backward passes.
