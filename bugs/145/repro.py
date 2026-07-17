from __future__ import annotations

import importlib.metadata as metadata
import math
import os
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "codebase"))

from sentence_transformers import SentenceTransformer
from sentence_transformers.models import StaticEmbedding


def version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def main() -> None:
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    print("sentence-transformers", version("sentence-transformers"))
    print("model2vec", version("model2vec"))
    print("transformers", version("transformers"))
    print("tokenizers", version("tokenizers"))
    print("huggingface-hub", version("huggingface-hub"))
    print("torch", torch.__version__)
    print("cuda_available", torch.cuda.is_available())

    static_embedding = StaticEmbedding.from_distillation("BAAI/bge-base-en-v1.5", device="cuda")
    model = SentenceTransformer(modules=[static_embedding])

    texts = [
        "What are Pandas?",
        "The giant panda (Ailuropoda melanoleuca; Chinese: 大熊猫; pinyin: dàxióngmāo), also known as the panda bear or simply the panda, is a bear native to south central China.",
    ]
    embeddings = model.encode(texts)
    similarity = model.similarity(embeddings[0], embeddings[1])
    observed = float(similarity.item())

    print("embedding_shape", tuple(embeddings.shape))
    print("similarity", similarity)

    expected = 0.9177
    observed_expected = 0.5375
    print("docstring_expected", expected)
    print("observed_expected", observed_expected)

    if not math.isclose(observed, observed_expected, rel_tol=0.0, abs_tol=1e-4):
        raise SystemExit(f"unexpected similarity: {observed} != {observed_expected}")


if __name__ == "__main__":
    main()
