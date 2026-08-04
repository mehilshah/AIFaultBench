#!/usr/bin/env bash
# Recreate this bug's codebase (the dataset does not ship it).
set -euo pipefail
git clone https://github.com/influxdata/influxdb-client-python codebase
git -C codebase checkout 1ec64b7e1039c891ac3a667ee6697731c61ddbaf
# then: bash setup_env.sh && bash run_repro.sh
