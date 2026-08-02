#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/langchain-ai/langchain codebase
git -C codebase checkout 73160209c3e60a8311f6e3402686d8982d735f83
# then: bash setup_env.sh && bash run_repro.sh
