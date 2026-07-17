from __future__ import annotations

import pathlib
import traceback
from types import SimpleNamespace

import requests
import torch
from safetensors.torch import save_file

from diffusers.loaders.lora_pipeline import StableDiffusionXLLoraLoaderMixin


ROOT = pathlib.Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
VALID_CHECKPOINT = ARTIFACTS_DIR / "valid_lora.safetensors"
OFFENDING_CHECKPOINT = ARTIFACTS_DIR / "detailed_notrigger.safetensors"
OFFENDING_URL = "https://huggingface.co/jagat334433/beru_custom/resolve/main/detailed_notrigger.safetensors"


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def download_file(url: str, destination: pathlib.Path) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        return

    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    with destination.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                handle.write(chunk)


def make_valid_lora_checkpoint(destination: pathlib.Path) -> None:
    if destination.exists() and destination.stat().st_size > 0:
        return

    state_dict = {
        "example.lora_A.weight": torch.zeros((1, 1), dtype=torch.float32),
        "example.lora_B.weight": torch.zeros((1, 1), dtype=torch.float32),
    }
    save_file(state_dict, str(destination))


class DummyPipeline(StableDiffusionXLLoraLoaderMixin):
    def __init__(self) -> None:
        self.unet = SimpleNamespace(config=SimpleNamespace())
        self.text_encoder = SimpleNamespace()
        self.text_encoder_2 = SimpleNamespace()

    def load_lora_into_unet(self, *args, **kwargs):  # noqa: D401 - intentionally no-op
        return None

    def load_lora_into_text_encoder(self, *args, **kwargs):  # noqa: D401 - intentionally no-op
        return None


def main() -> int:
    ensure_dir(ARTIFACTS_DIR)
    make_valid_lora_checkpoint(VALID_CHECKPOINT)
    download_file(OFFENDING_URL, OFFENDING_CHECKPOINT)

    pipe = DummyPipeline()
    pipe.load_lora_weights(str(VALID_CHECKPOINT), adapter_name="lora-add-detail-xl")

    try:
        pipe.load_lora_weights(str(OFFENDING_CHECKPOINT), adapter_name="lora-detailed_notrigger")
    except ValueError as exc:
        print("REPRODUCED: load_lora_weights rejected the real checkpoint.")
        print(f"ERROR: {exc}")
        traceback.print_exc()
        return 0

    print("Unexpected success: the offending checkpoint loaded without raising.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
