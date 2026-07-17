#!/usr/bin/env bash
set -euo pipefail

if command -v codon >/dev/null 2>&1; then
  echo "codon: $(command -v codon)"
  codon --version
  exit 0
fi

if [[ -x "${HOME}/.codon/bin/codon" ]]; then
  echo "${HOME}/.codon/bin/codon"
  "${HOME}/.codon/bin/codon" --version
  exit 0
fi

echo "codon binary not found on PATH or at ${HOME}/.codon/bin/codon" >&2
exit 1
