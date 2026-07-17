# Reproduction Trajectory — Bug 411: peft

- **Bug report:** [https://github.com/huggingface/peft/issues/602](https://github.com/huggingface/peft/issues/602)
- **Repository:** huggingface/peft @ `08cb3dde577747f6ca6638c884fd66fd16cf2e9d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Run bash run_repro.sh in the standardized folder.
2. The control case loads bigscience/bloomz-560m without device_map and confirms original_module_has_grad=False and modules_to_save_has_grad=True.
3. The offloaded case loads the same model with device_map='auto', max_memory={'cpu': '1600MB'}, and an offload folder.
4. Calling the wrapped score head triggers accelerate's offload hook and raises KeyError: 'score.weight'.

## Observed behavior

- Control run without device_map routed gradients to modules_to_save.default, while the offloaded device_map='auto' run on bigscience/bloomz-560m failed inside accelerate with KeyError: 'score.weight' when the PEFT ModulesToSaveWrapper forwarded through the classifier head.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
