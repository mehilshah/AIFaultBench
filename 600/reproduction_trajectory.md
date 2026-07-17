# Reproduction Trajectory — Bug 600: vllm

- **Bug report:** [https://github.com/vllm-project/vllm/issues/46988](https://github.com/vllm-project/vllm/issues/46988)
- **Repository:** vllm-project/vllm @ `5274c1181dc61bdf6e5eb610d37ebef694b1340d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a local synthetic test video with 250 frames at 25 FPS.
2. Executed the buggy metadata helpers from `codebase/vllm/assets/video.py` logic.
3. Compared reported metadata against the real video properties and sampled frame indices.

## Observed behavior

- Running `bash setup_env.sh && bash run_repro.sh` on a local 250-frame, 25 FPS synthetic video produced `actual_fps: 25.0` and buggy metadata with `fps: 0.3125`, `frames_indices: [0, 1, 2, ... 31]`, and `reported_timestamps_first_5: ["00:00", "00:03", "00:06", "00:09", "00:12"]`. The sampled frame indices expected from the code's own `np.linspace(...)` logic were `[0, 8, 16, 24, 32]`, so both the reported FPS and reported frame indices are wrong.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
