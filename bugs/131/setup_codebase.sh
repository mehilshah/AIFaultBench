#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/flairNLP/flair codebase
git -C codebase checkout 9f403b9dc29ec60c9736b10e52280686da75c015
# then: bash setup_env.sh && bash run_repro.sh
