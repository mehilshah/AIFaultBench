#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/SWE-agent/SWE-agent codebase
git -C codebase checkout c9a6634873077e7dc2bb77d72cf16091b5679ccd
# then: bash setup_env.sh && bash run_repro.sh
