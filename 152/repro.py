#!/usr/bin/env python3
import os

os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TQDM_DISABLE", "1")

import torch
from transformers import AutoTokenizer, pipeline


MODEL_ID = "naver-clova-ix/donut-base-finetuned-docvqa"
IMAGE_URL = (
    "https://huggingface.co/spaces/impira/docquery/resolve/"
    "2359223c1837a7587402bda0f2643382a6eefeab/invoice.png"
)
QUESTION = "What is the invoice number?"


def main() -> None:
    pipe = pipeline(
        "document-question-answering",
        model=MODEL_ID,
        tokenizer=AutoTokenizer.from_pretrained(MODEL_ID),
        image_processor=MODEL_ID,
        dtype=torch.float16,
    )

    print(f"decoder_start_token_id={pipe.model.config.decoder_start_token_id!r}")
    print(f"bos_token_id={pipe.model.config.bos_token_id!r}")
    result = pipe(image=IMAGE_URL, question=QUESTION)
    print(result)


if __name__ == "__main__":
    main()
