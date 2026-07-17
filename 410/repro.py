#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "codebase" / "vllm" / "model_executor" / "models" / "qwen3_asr_realtime.py"


class Qwen3ASRRealtimeBuffer:
    """Minimal copy of the realtime buffer logic from the source tree."""

    def __init__(self, sampling_rate: int, segment_duration_s: float = 5.0):
        self._sampling_rate = sampling_rate
        self._segment_size = int(segment_duration_s * sampling_rate)
        self._buffer_size = 60 * sampling_rate
        self._buffer = np.empty(self._buffer_size, dtype=np.float32)
        self._filled_len = 0

    def write_audio(self, audio: np.ndarray) -> None:
        put_end = self._filled_len + len(audio)
        if put_end > self._buffer_size:
            new_size = max(self._buffer_size * 2, put_end)
            new_buffer = np.empty(new_size, dtype=np.float32)
            new_buffer[: self._filled_len] = self._buffer[: self._filled_len]
            self._buffer = new_buffer
            self._buffer_size = new_size

        self._buffer[self._filled_len : put_end] = audio
        self._filled_len = put_end

    def read_audio(self) -> np.ndarray | None:
        if self._filled_len < self._segment_size:
            return None

        segment = self._buffer[: self._segment_size].copy()
        remaining = self._filled_len - self._segment_size
        if remaining > 0:
            self._buffer[:remaining] = self._buffer[
                self._segment_size : self._filled_len
            ]
        self._filled_len = remaining
        return segment

    def flush(self) -> np.ndarray | None:
        if self._filled_len == 0:
            return None
        audio = self._buffer[: self._filled_len].copy()
        self._filled_len = 0
        return audio


def simulate_streaming_split(
    duration_s: float = 10.0,
    sampling_rate: int = 16_000,
    input_chunk_s: float = 0.5,
) -> list[int]:
    total_samples = int(duration_s * sampling_rate)
    chunk_samples = int(input_chunk_s * sampling_rate)
    audio = np.linspace(-1.0, 1.0, total_samples, dtype=np.float32)

    buffer = Qwen3ASRRealtimeBuffer(sampling_rate=sampling_rate)
    segment_lengths: list[int] = []

    for start in range(0, total_samples, chunk_samples):
        buffer.write_audio(audio[start : start + chunk_samples])
        while (segment := buffer.read_audio()) is not None:
            segment_lengths.append(len(segment))

    remaining = buffer.flush()
    if remaining is not None:
        segment_lengths.append(len(remaining))

    return segment_lengths


def main() -> int:
    source_text = SOURCE.read_text(encoding="utf-8")
    hard_coded = "segment_duration_s = 5.0" in source_text
    segment_lengths = simulate_streaming_split()
    sr = 16_000
    segment_seconds = [round(n / sr, 3) for n in segment_lengths]

    print("Source inspected:", SOURCE)
    print("Hard-coded 5-second realtime segmenting:", hard_coded)
    print("Simulated input: 10.0s of audio fed in 0.5s chunks")
    print("Output segment lengths (samples):", segment_lengths)
    print("Output segment lengths (seconds):", segment_seconds)
    print(
        "Interpretation: the realtime path intentionally emits 5-second chunks, "
        "so a single utterance can surface as multiple streamed segments."
    )
    print(
        json.dumps(
            {
                "hard_coded_segment_duration_s": 5.0 if hard_coded else None,
                "segment_lengths_samples": segment_lengths,
                "segment_lengths_seconds": segment_seconds,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
