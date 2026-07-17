#!/usr/bin/env bash
set -euo pipefail

# Minimal environment bootstrap for this negative repro.
# The script does not depend on third-party Python packages.
python3 -V
