#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/pyro-ppl/pyro codebase
git -C codebase checkout c00bcc3fb701327b07e94de88754da49b7f29ebe
# then: bash setup_env.sh && bash run_repro.sh
