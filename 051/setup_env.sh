#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [ ! -d "${VENV_DIR}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

# Install the TensorFlow stack first, then pin the older standalone Keras and
# KerasNLP releases used in the bug report. pip's resolver refuses this mix in
# a single transaction, so we install it in stages.
python -m pip install tensorflow==2.20.0 tensorflow-text==2.20.1
python -m pip install --no-deps keras==3.2.1
python -m pip install --no-deps keras-nlp==0.14.4
python -m pip install absl-py dm-tree h5py kagglehub ml-dtypes namex optree regex rich

cat > "${VENV_DIR}/.bug_env" <<'EOF'
KERAS_BACKEND=tensorflow
EOF

echo "virtualenv ready at ${VENV_DIR}"
