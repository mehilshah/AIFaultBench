#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"
echo "No environment setup is required for this blocker repro."
echo "The local codebase does not contain the enterprise ColumnFormula constraint."
