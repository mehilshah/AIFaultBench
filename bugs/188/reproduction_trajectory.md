# Reproduction Trajectory — Bug 188: torchtune

- **Bug report:** [https://github.com/meta-pytorch/torchtune/issues/2828](https://github.com/meta-pytorch/torchtune/issues/2828)
- **Repository:** meta-pytorch/torchtune @ `2344509`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a clean virtual environment and install torch 2.7.1+cpu plus tensordict 0.13.0.
2. Load torchtune/dev/rl/datatypes/request_output.py through a fake vLLM dataclass stub.
3. Call RequestOutput.from_request_output() once with set_list_to_stack(False) and once with set_list_to_stack(True).
4. Observe the baseline succeeds and the list-to-stack case raises KeyError: tensor(10).

## Observed behavior

- Running bash ./run_repro.sh exits with status 1.
- repro_stdout.log shows set_list_to_stack(False): ok and set_list_to_stack(True): KeyError: tensor(10).
- repro_stderr.log shows the exception originates in torchtune/dev/rl/datatypes/request_output.py inside RequestOutput.__post_init__.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash ./run_repro.sh
```
