# Reproduction Trajectory — Bug 307: detectron2

- **Bug report:** [https://github.com/facebookresearch/detectron2/issues/3486](https://github.com/facebookresearch/detectron2/issues/3486)
- **Repository:** facebookresearch/detectron2 @ `ce5b1c5afe93919d14adf0fef27d608300a5171e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Load detectron2/utils/visualizer.py with local stubs for unrelated imports
2. Call draw_instance_predictions with instance_mode=ColorMode.IMAGE_BW on a synthetic mask
3. Compare the updated image buffer to VisImage.get_image()

## Observed behavior

- v.output.img[8,8] becomes [85, 85, 85] but v.output.get_image()[8,8] stays [255, 0, 0]. That means IMAGE_BW updates the buffer, but the rendered canvas still uses the original image.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
