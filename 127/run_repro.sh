#!/usr/bin/env bash
set -euo pipefail

CODON_BIN="${CODON_BIN:-$(command -v codon 2>/dev/null || true)}"
if [[ -z "${CODON_BIN}" && -x "${HOME}/.codon/bin/codon" ]]; then
  CODON_BIN="${HOME}/.codon/bin/codon"
fi

if [[ -z "${CODON_BIN}" ]]; then
  echo "codon binary not found" >&2
  exit 1
fi

"${CODON_BIN}" run repro.py
