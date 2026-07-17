#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/facebookresearch/fairseq codebase
git -C codebase checkout af12c9c6407bbcf2bca0b2f1923cf78f3db8857c
# then: bash setup_env.sh && bash run_repro.sh
