#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/transformers codebase
git -C codebase checkout 471d7ce9abbb3bc1b3bab673367378f9dbc3caac
# then: bash setup_env.sh && bash run_repro.sh
