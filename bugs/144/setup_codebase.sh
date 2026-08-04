#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/sentence-transformers codebase
git -C codebase checkout 348190d46b0c010c7a4693f198f0ddf70c6ceb35
# then: bash setup_env.sh && bash run_repro.sh
