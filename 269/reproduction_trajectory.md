# Reproduction Trajectory — Bug 269: lightning

- **Bug report:** [https://github.com/Lightning-AI/pytorch-lightning/issues/21822](https://github.com/Lightning-AI/pytorch-lightning/issues/21822)
- **Repository:** Lightning-AI/pytorch-lightning @ `eea74433ce552f962d3e345f138c5fa7de723638`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a checkpoint with only tensor state_dict data and a string _instantiator in hyper_parameters.
2. Verified torch.load(checkpoint, weights_only=True) succeeded on that checkpoint.
3. Called LightningModule.load_from_checkpoint() and observed the payload module import and function call via filesystem markers.

## Observed behavior

- torch.load(..., weights_only=True) returned plain checkpoint keys while Victim.load_from_checkpoint() imported payloadpkg.payload and executed it; the repro created both imported.txt and called.txt markers.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
