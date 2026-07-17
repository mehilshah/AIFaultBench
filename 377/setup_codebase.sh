#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/huggingface/diffusers codebase
git -C codebase checkout 7bf00006aa005eae37bcc639fd0f010c183365b4
# then: bash setup_env.sh && bash run_repro.sh
