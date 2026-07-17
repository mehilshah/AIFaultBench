from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase" / "src"))

from transformers.models.phi4_multimodal.configuration_phi4_multimodal import (  # noqa: E402
    Phi4MultimodalAudioConfig,
    Phi4MultimodalConfig,
    Phi4MultimodalVisionConfig,
)


def describe(label: str, config: Phi4MultimodalConfig) -> None:
    print(f"{label}:")
    print(f"  vision_config_type={type(config.vision_config).__name__}")
    print(f"  vision_config_is_none={config.vision_config is None}")
    print(f"  audio_config_type={type(config.audio_config).__name__}")
    print(f"  audio_config_is_none={config.audio_config is None}")


def main() -> None:
    failures: list[str] = []

    default_config = Phi4MultimodalConfig()
    describe("default_config", default_config)
    if default_config.vision_config is None:
        failures.append("Phi4MultimodalConfig() leaves vision_config as None.")
    if not isinstance(default_config.audio_config, Phi4MultimodalAudioConfig):
        failures.append("Phi4MultimodalConfig() did not create a default audio_config.")

    vision_only_config = Phi4MultimodalConfig(vision_config=Phi4MultimodalVisionConfig())
    describe("vision_only_config", vision_only_config)
    if vision_only_config.audio_config is None:
        failures.append(
            "Phi4MultimodalConfig(vision_config=Phi4MultimodalVisionConfig()) leaves audio_config as None."
        )

    if failures:
        raise AssertionError("\n".join(failures))

    print("No bug reproduced.")


if __name__ == "__main__":
    main()
