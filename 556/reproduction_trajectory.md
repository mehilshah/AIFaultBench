# Reproduction Trajectory — Bug 556: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46821](https://github.com/huggingface/transformers/issues/46821)
- **Repository:** huggingface/transformers @ `123f5dd72644728722a970b3e3ad1445cf620470`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Install dependencies with setup_env.sh
2. Run repro.py against the local codebase/ checkout
3. Pass window_size=5 into TimesFm2_5ModelForPrediction.forward()

## Observed behavior

- Traceback (most recent call last):
  File "repro.py", line 48, in <module>
    main()
  File "repro.py", line 44, in main
    model(past_values=past_values, window_size=5)
  File ".venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1736, in _wrapped_call_impl
    return self._call_impl(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1747, in _call_impl
    return forward_call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/transformers/utils/generic.py", line 907, in wrapper
    output = func(self, *args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "codebase/src/transformers/models/timesfm2_5/modeling_timesfm2_5.py", line 780, in forward
    new_inputs.extend(self._timesfm_moving_average(ts, window_size))
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File ".venv/lib/python3.12/site-packages/torch/nn/modules/module.py", line 1931, in __getattr__
    raise AttributeError(
AttributeError: 'TimesFm2_5ModelForPrediction' object has no attribute '_timesfm_moving_average'. Did you mean: '_timesfm2_5_moving_average'?

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
