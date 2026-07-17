import os
import sys
import traceback


os.environ.setdefault("KERAS_BACKEND", "tensorflow")

import keras
import keras_nlp


def main() -> int:
    keras.mixed_precision.set_global_policy("mixed_float16")
    print(f"backend={keras.backend.backend()}")
    print(f"policy={keras.mixed_precision.global_policy()}")
    print("loading preset=bert_tiny_en_uncased_sst2")
    try:
        keras_nlp.models.BertClassifier.from_preset("bert_tiny_en_uncased_sst2")
    except Exception:
        print("from_preset failed", file=sys.stderr)
        traceback.print_exc()
        return 1

    print("from_preset succeeded unexpectedly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
