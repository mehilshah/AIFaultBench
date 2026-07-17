# Reproduction Trajectory — Bug 543: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46829](https://github.com/huggingface/transformers/issues/46829)
- **Repository:** huggingface/transformers @ `4363936534ef47721b84a95bfdc758f056c3ee98`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create and activate the isolated virtual environment with bash setup_env.sh.
2. Run bash run_repro.sh with the local codebase on PYTHONPATH.
3. Observe that VideoPrismForVideoClassification returns a Tensor in outputs.hidden_states instead of None or a tuple.

## Observed behavior

- Running the local repro under an isolated CPU-only torch environment prints hidden_states_type=<class 'torch.Tensor'>, hidden_states_is_none=False, and hidden_states_is_tuple=False. The run then fails with AssertionError: FAIL: hidden_states is <class 'torch.Tensor'>, expected None or tuple. The captured traceback is in repro_stderr.log.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
