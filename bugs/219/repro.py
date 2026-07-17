import os

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

import tensorflow as tf
import transformers
from transformers import BertConfig, TFBertModel


def main() -> None:
    print(f"python: {os.sys.version.split()[0]}")
    print(f"tensorflow: {tf.__version__}")
    print(f"transformers: {transformers.__version__}")
    configuration = BertConfig(max_position_embeddings=2048)
    print("loading TFBertModel.from_pretrained('bert-base-uncased', config=BertConfig(max_position_embeddings=2048))")
    model = TFBertModel.from_pretrained("bert-base-uncased", config=configuration)
    print(type(model))


if __name__ == "__main__":
    main()

