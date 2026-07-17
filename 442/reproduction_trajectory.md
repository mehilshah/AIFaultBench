# Reproduction Trajectory — Bug 442: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/642](https://github.com/facebookresearch/detectron2/issues/642)
- **Repository:** facebookresearch/detectron2 @ `abae3ae4aaa6e9f5beb908b3b2f734cb12b38a9b`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Cloned the referenced detectron2 revision into codebase/.
2. Inspected the issue report and the model zoo recipe for Faster-RCNN R50-FPN 1x.
3. Compared detectron2/structures/image_list.py at HEAD against its parent commit.
4. Ran bash run_repro.sh to verify the current code path and capture logs.

## Observed behavior

- The checked-out detectron2 HEAD is abae3ae4aaa6e9f5beb908b3b2f734cb12b38a9b, which is the fix commit for the ImageList.from_tensors single-image zero-padding path.
- Current source at detectron2/structures/image_list.py:84-93 contains the zero-padding guard `if all(x == 0 for x in padding_size)` and uses non-inplace `unsqueeze(0)` in that branch.
- The parent commit (the pre-fix version referenced by the issue report) used the in-place `unsqueeze_` path for the single-image case.
- MODEL_ZOO.md still documents the Faster-RCNN R50-FPN 1x baseline as 37.9 AP, so the issue report is about reproducing that published recipe, but the local source tree already includes the relevant fix.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

This standardized folder already checks out the post-fix detectron2 commit, so the bug reported against the older pre-fix revision is not reproducible here. The original issue also depends on a full COCO training/evaluation run that is not bundled in this folder.
