# Reproduction Trajectory — Bug 014: models

- **Bug report:** [https://github.com/tensorflow/models/issues/11076](https://github.com/tensorflow/models/issues/11076)
- **Repository:** tensorflow/models @ `47571f3b2247b68a4370a3dd7c659d87e0affcad`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Generate Python protobuf modules from codebase/research/object_detection/protos/*.proto.
2. Create an empty TrainEvalPipelineConfig and merge a minimal pipeline config string.
3. Attempt to assign max_number_of_boxes on pipeline_config.eval_input_reader, which is a repeated container.

## Observed behavior

- 'google._upb._message.RepeatedCompositeContainer' object has no attribute 'max_number_of_boxes'

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
