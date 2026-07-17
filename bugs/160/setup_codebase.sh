#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/influxdata/influxdb-client-python codebase
git -C codebase checkout eb5afd1
# then: bash setup_env.sh && bash run_repro.sh
