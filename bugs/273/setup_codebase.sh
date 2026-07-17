#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 2bc97c02b777f17b371510f2fa4d672519664198
# then: bash setup_env.sh && bash run_repro.sh
