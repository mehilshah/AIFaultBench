# Bug 600 Reproduction

This folder reproduces the Gemma4 video metadata mismatch described in
`bug_report.txt`.

The repro is self-contained:

1. Generate a local 250-frame video at 25 FPS.
2. Run the buggy `video_to_ndarrays()` / `video_get_metadata()` logic from
   `codebase/vllm/assets/video.py`.
3. Show that the reported metadata is wrong:
   - reported FPS is `duration / num_frames`, not the real video FPS
   - reported `frames_indices` are `0..num_frames-1`, not the sampled indices
   - the second timestamp becomes `00:03`, matching the issue report

Run locally:

```bash
bash setup_env.sh
bash run_repro.sh
```

Run in Docker:

```bash
```

Generated artifacts:

- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Notes:

- The repro is based on the local implementation in
  `codebase/vllm/assets/video.py`.
- It does not require the full vLLM import stack; the mismatch is visible in
  the standalone video metadata helpers.
