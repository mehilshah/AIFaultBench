from __future__ import annotations

import torch
from datasets import load_dataset

import sentence_transformers
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator, SimilarityFunction


def main() -> None:
    print(f"sentence_transformers_version={sentence_transformers.__version__}")
    print(f"torch_version={torch.__version__}")
    print(f"cuda_available={torch.cuda.is_available()}")

    eval_dataset = load_dataset("sentence-transformers/stsb", split="validation")
    print(f"dataset_split=validation dataset_len={len(eval_dataset)}")
    print(f"sentence1_column_type={type(eval_dataset['sentence1']).__name__}")

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2", device="cuda")
    print(f"model_device={model.device}")

    evaluator = EmbeddingSimilarityEvaluator(
        sentences1=eval_dataset["sentence1"],
        sentences2=eval_dataset["sentence2"],
        scores=eval_dataset["score"],
        main_similarity=SimilarityFunction.COSINE,
        show_progress_bar=False,
    )

    result = evaluator(model)
    print(result)
    print(f"primary_metric={evaluator.primary_metric}")


if __name__ == "__main__":
    main()
