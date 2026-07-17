#!/usr/bin/env bash
set -euo pipefail

if command -v codon >/dev/null 2>&1; then
  exit 0
fi

if [ -x "$HOME/.codon/bin/codon" ]; then
  export PATH="$HOME/.codon/bin:$PATH"
  exit 0
fi

echo "error: codon is required but was not found on PATH or in ~/.codon/bin" >&2
exit 1
