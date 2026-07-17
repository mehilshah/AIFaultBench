#!/usr/bin/env bash
set -euo pipefail

# The repro is pure Python and uses only the standard library.
# Keep this script so the bundle has a standard setup entrypoint.
python3 --version
