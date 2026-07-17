#!/usr/bin/env python3
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main() -> int:
    print(f"torch={torch.__version__}")
    print("loading pretrained gpt2")

    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.generation_config.cache_implementation = "static"
    model.forward = torch.compile(model.forward, backend="inductor")

    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    input_ids = tokenizer("Hello world", return_tensors="pt").input_ids
    print(f"input_shape={tuple(input_ids.shape)}")

    print("first generate() call")
    output1 = model.generate(input_ids, max_new_tokens=1, do_sample=False)
    print(f"first_output_shape={tuple(output1.shape)}")
    print(f"first_output={output1.tolist()}")

    print("second generate() call")
    output2 = model.generate(input_ids, max_new_tokens=1, do_sample=False)
    print(f"second_output_shape={tuple(output2.shape)}")
    print(f"second_output={output2.tolist()}")
    print("repro_status=not_reproduced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
