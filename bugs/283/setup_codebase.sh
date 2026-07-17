#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 498d6e984e84d29186e671656817a53a024af930
# then: bash setup_env.sh && bash run_repro.sh
