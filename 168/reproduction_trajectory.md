# Reproduction Trajectory — Bug 168: kornia

- **Bug report:** [https://github.com/kornia/kornia/issues/3194](https://github.com/kornia/kornia/issues/3194)
- **Repository:** kornia/kornia @ `9cea9ae`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a 2-video tensor with 20 identical frames per video.
2. Apply `VideoSequential(RandomCrop(size=(50, 50), same_on_batch=False), data_format="BCTHW", same_on_frame=True)`.
3. Apply `VideoSequential(RandomHorizontalFlip(p=1.0, same_on_batch=False), data_format="BCTHW", same_on_frame=True)`.
4. Apply both transforms together in one `VideoSequential` pipeline.

## Observed behavior

- Running `bash run_repro.sh` reproduced the issue in this snapshot. `RandomCrop` produced `frames_identical: [False, False]` and `videos_different: False`; `RandomHorizontalFlip` produced `frames_identical: [True, True]` and `videos_different: False`; the combined pipeline also failed the batch-level separation check.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
