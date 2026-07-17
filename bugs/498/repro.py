#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch
from diffusers import QwenImageEditPipeline
from diffusers.utils import load_image


ROOT = Path(__file__).resolve().parent
OUT_IMAGE = ROOT / "qwenimage_edit.png"
RESULT = ROOT / "reproduction.json"


def main() -> int:
    result = {
        "reproducible": False,
        "evidence": "",
        "steps": [
            "Load QwenImageEditPipeline from Qwen/Qwen-Image-Edit with torch.bfloat16.",
            "Run the documentation snippet against the yarn-art Pikachu input image.",
            "Inspect the saved image statistics to determine whether the output is black.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    try:
        print(f"python={sys.version.split()[0]}")
        print(f"torch={torch.__version__}")
        print(f"cuda_available={torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"cuda_device={torch.cuda.get_device_name(0)}")

        pipe = QwenImageEditPipeline.from_pretrained(
            "Qwen/Qwen-Image-Edit",
            torch_dtype=torch.bfloat16,
        )
        try:
            pipe.to("cuda")
            print("device_mode=to(cuda)")
        except torch.OutOfMemoryError as exc:
            print(f"device_mode=cpu_offload fallback ({exc.__class__.__name__})")
            pipe.enable_model_cpu_offload()

        image = load_image(
            "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/diffusers/yarn-art-pikachu.png"
        ).convert("RGB")
        prompt = "Make Pikachu hold a sign that says 'Qwen Edit is awesome', yarn art style, detailed, vibrant colors"

        output = pipe(image, prompt, num_inference_steps=50).images[0]
        output.save(OUT_IMAGE)

        arr = np.asarray(output)
        stats = {
            "shape": list(arr.shape),
            "dtype": str(arr.dtype),
            "min": int(arr.min()),
            "max": int(arr.max()),
            "mean": float(arr.mean()),
            "sum": int(arr.sum()),
        }
        print(json.dumps(stats, indent=2))
        print(f"saved={OUT_IMAGE}")

        black = stats["max"] == 0 and stats["sum"] == 0
        result["reproducible"] = black
        result["evidence"] = (
            "The docs snippet generated an all-black image (uint8 max=0, sum=0)."
            if black
            else "The generated image was not all black in this environment."
        )
        result["blocking_reason"] = "" if black else "No black image was produced in this environment."
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return 0 if black else 1
    except Exception as exc:
        result["reproducible"] = False
        result["evidence"] = f"Reproduction could not be completed: {exc.__class__.__name__}: {exc}"
        result["blocking_reason"] = "The reproduction environment failed before the QwenImageEditPipeline call finished."
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        raise


if __name__ == "__main__":
    raise SystemExit(main())
