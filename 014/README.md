# Bug 014

This folder contains a self-contained reproduction bundle for TensorFlow Models issue 11076.

Inputs:
- `bug_report.txt`
- `codebase/`

Generated artifacts:
- `repro.py`
- `requirements.txt`
- `setup_env.sh`
- `run_repro.sh`
- `reproduction.json`
- `repro_stdout.log`
- `repro_stderr.log`

Reproduction command:
- `bash run_repro.sh`

What the repro does:
- compiles the local `object_detection/protos/*.proto` files into a temporary Python package
- parses a minimal `TrainEvalPipelineConfig`
- attempts `pipeline_config.eval_input_reader.max_number_of_boxes = 500`
- captures the resulting `AttributeError`
