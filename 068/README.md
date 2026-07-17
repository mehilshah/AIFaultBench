# Bug 068

Reproduction bundle for:
`https://github.com/keras-team/keras-io/issues/1475`

The failure is in `keras_cv.metrics.BoxCOCOMetrics.result(force=True)` when the metric has accumulated batches with different numbers of boxes per image. The concat step in `_box_concat()` assumes the non-batch dimensions match across all cached batches and crashes when they do not.

Reproduction summary:
- environment: Python 3.12
- tested versions: `tensorflow-cpu==2.21.0`, `keras-cv==0.9.0`
- trigger: two metric updates with shapes `[4, 2, 4]` and `[4, 1, 4]`
- observed failure: `InvalidArgumentError: ConcatOp : Dimension 1 in both shapes must be equal`

Files in this bundle:
- `bug_report.txt`
- `codebase/`
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`
