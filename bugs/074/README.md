# DeepSpeed-Chat actor-loss mask repro

This folder contains a minimal, deterministic reproduction of the masking bug
described in `bug_report.txt`.

## What it shows

In `codebase/applications/DeepSpeed-Chat/dschat/rlhf/ppo_trainer.py`, the
terminal reward is attached using:

```python
ends = start + action_mask[:, start:].sum(1) + 1
rewards[j, start:ends[j]][-1] += reward_clip[j]
```

The same step later trains with:

```python
actor_loss_fn(actor_log_prob[:, start:], log_probs[:, start:], advantages, action_mask[:, start:])
```

For a sequence shaped like `prompt + answer + eos + pad`, this places the
terminal reward on the padded slot, while `actor_loss_fn` masks that slot out.

## Run

```bash
bash setup_env.sh
bash run_repro.sh
```

The script prints a JSON payload showing:

* the reward target index used by the current implementation
* the EOS-aligned index that the reward should land on
* the mask values for both positions
* the resulting actor-loss delta versus a corrected alignment

## Expected outcome

The current implementation is reproducibly misaligned: the terminal reward is
attached to a masked padding position instead of the EOS action.
