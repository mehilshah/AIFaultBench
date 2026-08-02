#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout 2661b55323644eeaf56d133fc6fcb1580c6bcdee
# then: bash setup_env.sh && bash run_repro.sh
