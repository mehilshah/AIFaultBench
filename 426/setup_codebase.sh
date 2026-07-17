#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/peft codebase
git -C codebase checkout 3714aa2fff158fdfa637b2b65952580801d890b2
# then: bash setup_env.sh && bash run_repro.sh
