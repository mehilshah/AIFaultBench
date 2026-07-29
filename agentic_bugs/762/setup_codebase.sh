#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout a6b2dbd68fa46287aa061f2dc726c9fd6cb870d2
# then: bash setup_env.sh && bash run_repro.sh
