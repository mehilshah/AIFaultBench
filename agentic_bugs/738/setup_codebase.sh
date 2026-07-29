#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/Arize-ai/phoenix codebase
git -C codebase checkout 7afa18317c18142d7eb772682bc9369b10cf0e2e
# then: bash setup_env.sh && bash run_repro.sh
