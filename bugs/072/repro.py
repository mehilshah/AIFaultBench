#!/usr/bin/env python3
"""Minimal reproduction for the DeepSpeedEngine.model AttributeError."""


class DeepSpeedEngine:
    def __getattr__(self, name):
        raise AttributeError(
            f"'{type(self).__name__}' object has no attribute '{name}'")


def main():
    model = DeepSpeedEngine()

    # This mirrors the buggy access pattern in:
    # codebase/applications/DeepSpeed-Chat/training/step1_supervised_finetuning/main.py:367
    print("About to access model.model on a DeepSpeedEngine-like object")
    _ = model.model


if __name__ == "__main__":
    main()
