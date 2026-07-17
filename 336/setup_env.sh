#!/usr/bin/env bash
set -euo pipefail

# The harness only uses the Python standard library, so no installation step is
# required here. Keep the script so the bundle has the standard standardized shape.
python3 -V
