#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODON_BIN="${CODON_BIN:-codon}"

"${CODON_BIN}" run "${ROOT}/repro.py"
