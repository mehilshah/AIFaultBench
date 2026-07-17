#!/usr/bin/env bash
set -euo pipefail

echo "No additional environment setup is required."
command -v nvcc >/dev/null
nvcc --version | sed -n '1,5p'

