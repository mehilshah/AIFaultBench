#!/usr/bin/env python3
"""Reproduce the Gemma4 video metadata mismatch from vLLM.

This script mirrors the buggy logic in `codebase/vllm/assets/video.py`:

- `video_to_ndarrays()` samples frames with `np.linspace(...)`
- `video_get_metadata()` reports `fps = duration / num_frames`
  and `frames_indices = list(range(num_frames))`

The repro uses a locally generated video with a known FPS so the mismatch is
fully self-contained.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import cv2
import numpy as np


VIDEO_FPS = 25.0
TOTAL_FRAMES = 250
SAMPLED_FRAMES = 32
FRAME_SIZE = (64, 64)


def _write_test_video(path: Path) -> None:
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(str(path), fourcc, VIDEO_FPS, FRAME_SIZE)
    if not writer.isOpened():
        raise RuntimeError("Could not open OpenCV video writer")

    try:
        for idx in range(TOTAL_FRAMES):
            # Encode the frame index into RGB channels so the file is not empty
            # and each frame is distinct.
            frame = np.zeros((FRAME_SIZE[1], FRAME_SIZE[0], 3), dtype=np.uint8)
            frame[:, :, 0] = idx % 256
            frame[:, :, 1] = (idx * 3) % 256
            frame[:, :, 2] = (idx * 7) % 256
            writer.write(frame)
    finally:
        writer.release()


def video_to_ndarrays(path: str, num_frames: int = -1) -> np.ndarray:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file {path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames: list[np.ndarray] = []

    num_frames = num_frames if num_frames > 0 else total_frames
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    for idx in range(total_frames):
        ok = cap.grab()
        if not ok:
            break
        if idx in frame_indices:
            ret, frame = cap.retrieve()
            if ret:
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    frames = np.stack(frames)
    if len(frames) < num_frames:
        raise ValueError(
            f"Could not read enough frames from video file {path} "
            f"(expected {num_frames} frames, got {len(frames)})"
        )
    return frames


def video_get_metadata(path: str, num_frames: int = -1) -> dict[str, object]:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file {path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0

    if num_frames == -1 or num_frames > total_frames:
        num_frames = total_frames

    metadata = {
        "total_num_frames": num_frames,
        "fps": duration / num_frames,
        "duration": duration,
        "video_backend": "opencv",
        "frames_indices": list(range(num_frames)),
        "do_sample_frames": num_frames == total_frames,
    }
    return metadata


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="gemma4_video_repro_") as tmpdir:
        video_path = Path(tmpdir) / "sample.avi"
        _write_test_video(video_path)

        frames = video_to_ndarrays(str(video_path), SAMPLED_FRAMES)
        metadata = video_get_metadata(str(video_path), SAMPLED_FRAMES)

        cap = cv2.VideoCapture(str(video_path))
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        actual_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        expected_indices = np.linspace(
            0, actual_total - 1, SAMPLED_FRAMES, dtype=int
        ).tolist()
        reported_indices = metadata["frames_indices"]
        reported_fps = float(metadata["fps"])
        reported_timestamps = [
            f"{int((idx / reported_fps) // 60):02d}:{int((idx / reported_fps) % 60):02d}"
            for idx in reported_indices[:5]
        ]

        print(
            json.dumps(
                {
                    "video_path": str(video_path),
                    "actual_fps": actual_fps,
                    "actual_total_frames": actual_total,
                    "sampled_frames": int(frames.shape[0]),
                    "expected_sample_indices": expected_indices[:5],
                    "reported_metadata": metadata,
                    "reported_timestamps_first_5": reported_timestamps,
                },
                indent=2,
                sort_keys=True,
            )
        )

        assert actual_fps == VIDEO_FPS
        assert frames.shape[0] == SAMPLED_FRAMES
        assert reported_fps != actual_fps, (
            "Expected buggy metadata fps to differ from the real video fps"
        )
        assert reported_indices != expected_indices, (
            "Expected buggy metadata frame indices to differ from the sampled "
            "frame indices"
        )
        assert reported_timestamps[1] == "00:03", (
            "Expected the second reported timestamp to be `00:03`, matching "
            "the bug report"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
