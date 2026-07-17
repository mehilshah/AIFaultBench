from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "codebase"))

from sentence_transformers import SentenceTransformer, models  # noqa: E402


def main() -> int:
    model_name = "sshleifer/tiny-gpt2"
    word_embedding_model = models.Transformer(model_name_or_path=model_name)
    word_embedding_model.tokenizer.pad_token = word_embedding_model.tokenizer.eos_token
    pooling_model = models.Pooling(
        word_embedding_model.get_word_embedding_dimension(),
        pooling_mode="lasttoken",
        pooling_mode_lasttoken=True,
    )
    model = SentenceTransformer(modules=[word_embedding_model, pooling_model], device="cpu")

    print(json.dumps({"model_name": model_name, "sentence_transformers_path": str(REPO_ROOT / "codebase")}))

    tokenizer_outputs = {}
    encode_outputs = {}
    for text in ["test", " test"]:
        tokens = model.tokenizer(text, truncation=False, return_offsets_mapping=True)
        token_ids = list(tokens["input_ids"])
        decoded = model.tokenizer.decode(token_ids)
        tokenizer_outputs[text] = token_ids

        embedding = model.encode(text, normalize_embeddings=True, output_value="sentence_embedding")
        embedding = np.asarray(embedding)
        encode_outputs[text] = embedding

        print(f"text={text!r}")
        print(f"tokenizer.input_ids={token_ids}")
        print(f"tokenizer.decoded={decoded!r}")
        print(f"encode.shape={embedding.shape}")
        print(f"encode.head={embedding[:6].tolist()}")
        print()

    same_tokenizer = tokenizer_outputs["test"] == tokenizer_outputs[" test"]
    same_embedding = np.allclose(encode_outputs["test"], encode_outputs[" test"])
    max_diff = float(np.max(np.abs(encode_outputs["test"] - encode_outputs[" test"])))

    print(json.dumps(
        {
            "model.tokenizer_equal": same_tokenizer,
            "encode_equal": same_embedding,
            "max_abs_diff": max_diff,
        }
    ))

    if same_tokenizer:
        raise AssertionError("Expected the tokenizer to distinguish leading whitespace, but it did not.")
    if not same_embedding:
        raise AssertionError("Expected encode() to collapse whitespace-stripped inputs, but it did not.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
