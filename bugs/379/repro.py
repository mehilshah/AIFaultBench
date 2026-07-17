#!/usr/bin/env python3
import multiprocessing as mp
import os
import sys

import torch
import torch.nn as nn

from accelerate.big_modeling import dispatch_model


class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(4, 4)
        self.proj = nn.Linear(4, 2)

    def forward(self, x):
        return self.proj(self.embedding(x))


class ValidationProcess(mp.Process):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        print("child process started")


def run_case(label, model):
    print(f"CASE: {label}")
    proc = ValidationProcess(model)
    proc.start()
    proc.join()
    print(f"EXIT: {proc.exitcode}")
    return proc.exitcode


def main():
    print(f"python={sys.version.split()[0]}")
    print(f"torch={torch.__version__}")
    print(f"cwd={os.getcwd()}")
    print(f"start_method_before_set={mp.get_start_method(allow_none=True)}")

    mp.set_start_method("spawn", force=True)

    baseline = TinyModel()
    run_case("baseline model", baseline)

    dispatched = TinyModel()
    dispatched = dispatch_model(dispatched, {"": "cpu"})
    run_case('dispatch_model({"": "cpu"})', dispatched)


if __name__ == "__main__":
    main()
