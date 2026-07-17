#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/lucidrains/x-transformers codebase
git -C codebase checkout eeed50391855f8d552edc866701952f38015e415
# then: bash setup_env.sh && bash run_repro.sh
