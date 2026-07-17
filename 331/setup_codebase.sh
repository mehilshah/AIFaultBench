#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 0bc355418bb265136a66c2dedc501066ffbc237d
# then: bash setup_env.sh && bash run_repro.sh
