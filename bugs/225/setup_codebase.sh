#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/unclecode/crawl4ai codebase
git -C codebase checkout 4e1c4bd24e253755c8ce005680b8ef292d64216e
# then: bash setup_env.sh && bash run_repro.sh
