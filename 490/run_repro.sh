#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="detectron2-bug-490-repro"
STDOUT_LOG="$ROOT/repro_stdout.log"
STDERR_LOG="$ROOT/repro_stderr.log"

: >"$STDOUT_LOG"
: >"$STDERR_LOG"

{
  echo "Building repro image: $IMAGE"
  docker build -t "$IMAGE" -f "$ROOT/Dockerfile" "$ROOT"
  echo "Running repro container without GPU runtime"
  docker run --rm "$IMAGE"
} >>"$STDOUT_LOG" 2>>"$STDERR_LOG"
