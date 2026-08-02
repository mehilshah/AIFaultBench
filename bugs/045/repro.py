#!/usr/bin/env python3
from omegaconf import OmegaConf


def main() -> None:
    # This mirrors the shape of the structured config path used by fairseq's
    # generation/checkpoint loading code. The bug occurs when speech_to_speech
    # writes a new key onto a struct-locked model config.
    cfg = OmegaConf.create(
        {
            "task": {
                "_name": "speech_to_speech",
                "data": "/tmp/fake-data",
                "config_yaml": "config.yaml",
                "target_is_code": True,
                "target_code_size": 100,
                "vocoder": "code_hifigan",
                "n_frames_per_step": 1,
                "eval_inference": False,
                "infer_target_lang": "",
                "max_source_positions": 6000,
                "max_target_positions": 1024,
                "seed": 1,
            },
            "model": {
                "_name": "s2ut_transformer_fisher",
            },
        }
    )
    OmegaConf.set_struct(cfg, True)

    print("Attempting to write input_feat_per_channel onto a struct-locked model config")
    # This is the failing operation from the bug path.
    cfg.model.input_feat_per_channel = 80
    print("Unexpected success: the repro did not fail.")


if __name__ == "__main__":
    main()
