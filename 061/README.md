# Repro Bundle

This folder reproduces the KerasCV import error reported in
`bug_report.txt`.

The failure is triggered by loading `keras_cv/models/weights.py` from
KerasCV 0.4.0 in an environment with Keras 3:

`ImportError: cannot import name 'data_utils' from 'keras.utils'`

Use `./run_repro.sh` to create the virtualenv, install dependencies, and
run the reproduction.
