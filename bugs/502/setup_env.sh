#!/usr/bin/env bash
set -euo pipefail

# The repro harness is stdlib-only. Keep the setup step explicit so the bundle
# remains runnable in a fresh checkout, but do not install anything.
python3 --version
