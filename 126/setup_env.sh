#!/usr/bin/env bash
set -euo pipefail

if ! command -v codon >/dev/null 2>&1; then
  echo "codon is required but was not found in PATH" >&2
  exit 1
fi

codon --version
