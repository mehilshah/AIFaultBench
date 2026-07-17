#!/usr/bin/env python3
"""Reproduce blank word/segment timestamps from Canary-1B-V2 tensor-loaded audio."""

from __future__ import annotations

import json
import sys
import time
import zipfile
from pathlib import Path

import librosa

from nemo.collections.asr.models import EncDecMultiTaskModel


ROOT = Path(__file__).resolve().parent
ZIP_PATH = ROOT / "timestamp.zip"
WAV_PATH = ROOT / "timestamp.wav"


def ensure_audio() -> Path:
    if WAV_PATH.exists():
        return WAV_PATH

    if not ZIP_PATH.exists():
        raise FileNotFoundError("Missing timestamp.zip; cannot extract reporter audio.")

    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(ROOT)

    if not WAV_PATH.exists():
        raise FileNotFoundError("timestamp.wav was not extracted from timestamp.zip.")

    return WAV_PATH


def main() -> int:
    audio_path = ensure_audio()

    print(f"Loading model from_pretrained('nvidia/canary-1b-v2')", flush=True)
    model_start = time.time()
    model = EncDecMultiTaskModel.from_pretrained("nvidia/canary-1b-v2")
    print(f"Model loaded in {time.time() - model_start:.2f}s", flush=True)
    print(f"timestamps_asr_model is None: {model.timestamps_asr_model is None}", flush=True)

    audio, sr = librosa.load(audio_path, sr=16000)
    print(f"Loaded {audio_path.name}: {len(audio)} samples @ {sr} Hz", flush=True)

    start = time.time()
    hypotheses = model.transcribe(
        audio=audio,
        source_lang="fr",
        target_lang="fr",
        timestamps=True,
        batch_size=1,
        return_hypotheses=True,
    )
    elapsed = time.time() - start

    print(f"Transcription finished in {elapsed:.2f}s", flush=True)
    print(json.dumps([hyp.timestamp for hyp in hypotheses], indent=2, default=str), flush=True)

    observed = hypotheses[0].timestamp
    word_ts = observed.get("word") if isinstance(observed, dict) else None
    segment_ts = observed.get("segment") if isinstance(observed, dict) else None

    if word_ts or segment_ts:
        print("Unexpected: timestamps were populated; this environment did not reproduce the issue.", flush=True)
        return 1

    print("Reproduced: timestamp['word'] and timestamp['segment'] are both empty.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
