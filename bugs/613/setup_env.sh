#!/usr/bin/env bash
set -euo pipefail

# No package installation is required for this minimal repro.
# Preserve a stable working directory for the runner.
cd "$(dirname "$0")"
