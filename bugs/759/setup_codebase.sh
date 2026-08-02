#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pydantic/pydantic-ai codebase
git -C codebase checkout e19e18065a13be0490483ad3c5601d232af8185b
# then: bash setup_env.sh && bash run_repro.sh
