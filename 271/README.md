# Bug 271 Repro Bundle

This folder reproduces the DeepSpeed ZeRO-3 mixed-dtype all-gather regression
described in `bug_report.txt`.

The failure comes from the current `codebase/` logic in
`deepspeed/runtime/zero/partition_parameters.py`:

- output buffers for `_allgather_params_coalesced()` are allocated from
  `param_list[0].ds_tensor.dtype`
- if later persistent parameters are a different dtype, the gather target and
  source mismatch
- PyTorch raises `TypeError: output tensor must have the same type as input tensor`

The local `codebase/version.txt` reports DeepSpeed `0.19.3`, but the vulnerable
allocation pattern is still present in this snapshot.

## Files

- `repro.py`: minimal self-contained repro
- `requirements.txt`: runtime dependency list
- `setup_env.sh`: installs the Python dependencies
- `run_repro.sh`: runs the repro and writes `repro_stdout.log` / `repro_stderr.log`
- `reproduction.json`: machine-readable reproduction result

## Run

```bash
bash run_repro.sh
```

Expected outcome:

- exit code `1`
- stdout shows the mixed bf16 / fp32 persistent parameters
- stdout ends with `TypeError: output tensor must have the same type as input tensor`

## Source References

- `codebase/deepspeed/runtime/zero/partition_parameters.py:1925-1949`
- `codebase/deepspeed/runtime/engine.py:1364-1379`
- `codebase/deepspeed/runtime/zero/stage3.py:2391-2393`
