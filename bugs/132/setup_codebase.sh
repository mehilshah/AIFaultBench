#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/flairNLP/flair codebase
git -C codebase checkout 4d5ede757c1f2c569a0849c239202067911b64d8
# then: bash setup_env.sh && bash run_repro.sh
