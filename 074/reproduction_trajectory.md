# Reproduction Trajectory — Bug 074: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/888](https://github.com/deepspeedai/DeepSpeedExamples/issues/888)
- **Repository:** deepspeedai/DeepSpeedExamples @ `df7119ed264bfac747969f9bb5bed8a61aed5e5d`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read `bug_report.txt` and `codebase/applications/DeepSpeed-Chat/dschat/rlhf/ppo_trainer.py` to locate the reward-placement and actor-loss masking logic.
2. Ran `bash setup_env.sh && bash run_repro.sh` in the bug folder.
3. Observed that the current implementation attaches the terminal reward to a masked padding slot instead of the EOS action.

## Observed behavior

- The current DeepSpeed-Chat PPO code writes the terminal reward with `rewards[j, start:ends[j]][-1] += reward_clip[j]` while training with `actor_loss_fn(..., action_mask[:, start:])` in `codebase/applications/DeepSpeed-Chat/dschat/rlhf/ppo_trainer.py`.
- The repro output shows `current_reward_target_index` = 5 with `current_reward_target_mask_value` = 0, while the EOS-aligned index is 4 with `eos_mask_value` = 1.
- The current and corrected actor losses differ: `current_actor_loss` = -0.9032916666666666 vs `fixed_actor_loss` = -0.9508333333333333.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash setup_env.sh && bash run_repro.sh
```
