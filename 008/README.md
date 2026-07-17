# Bug 008

This folder is a self-contained reproduction bundle for TensorFlow Models issue
`#11141`.

Observed behavior
- The TF2 object detection TFLite exporter rejects Faster R-CNN configs with
  `ValueError: Only ssd or center_net models are supported in tflite.`
- This matches the implementation in
  [`codebase/research/object_detection/export_tflite_graph_lib_tf2.py`](codebase/research/object_detection/export_tflite_graph_lib_tf2.py)
  and the mobile-export docs in
  [`codebase/research/object_detection/g3doc/running_on_mobile_tf2.md`](codebase/research/object_detection/g3doc/running_on_mobile_tf2.md).

Bundle contents
- `repro.py`: minimal reproducer for the Faster R-CNN TF2 export guard.
- `run_repro.sh`: executes the reproducer.
- `setup_env.sh`: creates an isolated environment for reruns.
- `requirements.txt`: empty on purpose; the reproducer only uses the Python
  standard library.
- `manifest.json`: metadata used by the benchmark harness.
- `reproduction.json`: schema-constrained result written after running
  the repro.
- `repro_stdout.log` and `repro_stderr.log`: captured command output.

Reproduction command
`./run_repro.sh`
