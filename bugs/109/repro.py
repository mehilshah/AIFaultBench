import sys
import traceback

import torch

# Python 3.12 removed distutils from the stdlib. Accelerate still imports it
# through transformers, so provide a lightweight compatibility alias.
try:
    import setuptools._distutils as _distutils

    sys.modules.setdefault("distutils", _distutils)
except Exception:
    pass

from transformers import BertConfig, BertForSequenceClassification

from adapters import PrefixTuningConfig, init
import adapters.composition as ac


def run_case(batch_sizes):
    model = BertForSequenceClassification(BertConfig(num_hidden_layers=2))
    init(model)
    config = PrefixTuningConfig()
    model.add_adapter("a", config)
    model.add_adapter("b", config)
    model.active_adapters = ac.BatchSplit("a", "b", batch_sizes=batch_sizes)
    return model(input_ids=torch.randint(1000, (2, 128)))


def main():
    print("python", sys.version.replace("\n", " "))
    print("torch", torch.__version__)
    print("running failing case: batch_sizes=[2, 0]")
    try:
        run_case([2, 0])
    except Exception as exc:
        print(f"EXPECTED_FAILURE: {type(exc).__name__}: {exc}")
        traceback.print_exc()
    else:
        print("UNEXPECTED_SUCCESS: failing case did not raise")

    print("running control case: batch_sizes=[0, 2]")
    try:
        output = run_case([0, 2])
        print("CONTROL_SUCCESS:", tuple(output.logits.shape))
    except Exception as exc:
        print(f"CONTROL_FAILURE: {type(exc).__name__}: {exc}")
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
