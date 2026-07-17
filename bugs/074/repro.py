#!/usr/bin/env python3
"""Minimal reproduction of the actor-loss mask offset in DeepSpeed-Chat.

The current implementation in `dschat/rlhf/ppo_trainer.py`:

* computes the terminal reward index with `start + action_mask[:, start:].sum(1) + 1`
* then assigns the reward to `rewards[j, start:ends[j]][-1]`
* and later trains with `actor_loss_fn(..., action_mask[:, start:])`

For a sequence shaped like `prompt + answer + eos + pad`, that combination
places the terminal reward on the padded position, while the EOS position is
the last masked-in action. This script reproduces that mismatch with plain
Python lists.
"""

from __future__ import annotations

import json


def get_advantages_and_returns(values, rewards, start, gamma=1.0, lam=0.95):
    batch_size = len(rewards)
    length = len(rewards[0])
    advantages = [[0.0 for _ in range(length - start)] for _ in range(batch_size)]
    returns = [[0.0 for _ in range(length - start)] for _ in range(batch_size)]

    for b in range(batch_size):
        lastgaelam = 0.0
        reversed_advantages = []
        for t in reversed(range(start, length)):
            nextvalues = values[b][t + 1] if t < length - 1 else 0.0
            delta = rewards[b][t] + gamma * nextvalues - values[b][t]
            lastgaelam = delta + gamma * lam * lastgaelam
            reversed_advantages.append(lastgaelam)
        reversed_advantages.reverse()
        advantages[b] = reversed_advantages
        for i, adv in enumerate(reversed_advantages):
            returns[b][i] = adv + values[b][start + i]

    return advantages, returns


def actor_loss_fn(logprobs, old_logprobs, advantages, mask, cliprange=0.2):
    masked_terms = []
    mask_sum = 0.0
    for b in range(len(logprobs)):
        for i in range(len(logprobs[b])):
            log_ratio = (logprobs[b][i] - old_logprobs[b][i]) * mask[b][i]
            ratio = pow(2.718281828459045, log_ratio)
            pg_loss1 = -advantages[b][i] * ratio
            clipped = min(max(ratio, 1.0 - cliprange), 1.0 + cliprange)
            pg_loss2 = -advantages[b][i] * clipped
            masked_terms.append(max(pg_loss1, pg_loss2) * mask[b][i])
            mask_sum += mask[b][i]
    return sum(masked_terms) / mask_sum


def compute_rewards_current(prompts, log_probs, ref_log_probs, reward_score, action_mask, kl_ctl=0.1):
    start = len(prompts[0]) - 1
    rewards = [[-kl_ctl * (log_probs[b][i] - ref_log_probs[b][i]) for i in range(len(log_probs[b]))] for b in range(len(log_probs))]
    ends = [start + sum(action_mask[b][start:]) + 1 for b in range(len(action_mask))]
    for b in range(len(rewards)):
        rewards[b][ends[b] - 1] += reward_score[b]
    return rewards, ends


def compute_rewards_fixed(prompts, log_probs, ref_log_probs, reward_score, action_mask, kl_ctl=0.1):
    start = len(prompts[0]) - 1
    rewards = [[-kl_ctl * (log_probs[b][i] - ref_log_probs[b][i]) for i in range(len(log_probs[b]))] for b in range(len(log_probs))]
    for b in range(len(rewards)):
        eos_reward_index = start + sum(action_mask[b][start:]) - 1
        rewards[b][eos_reward_index] += reward_score[b]
    return rewards


def main():
    # Token layout:
    # [prompt_0, prompt_1, prompt_2, answer_0, answer_1, eos, pad]
    seq = [[101, 102, 103, 201, 202, 2, 0]]
    prompts = [row[:3] for row in seq]
    attention_mask = [[1 if token != 0 else 0 for token in row] for row in seq]
    action_mask = [row[1:] for row in attention_mask]

    # Use zero KL so the reward placement is easy to inspect.
    log_probs = [[0.0] * (len(seq[0]) - 1)]
    ref_log_probs = [[0.0] * (len(seq[0]) - 1)]
    reward_score = [1.0]
    values = [[0.0] * (len(seq[0]) - 1)]

    current_rewards, ends = compute_rewards_current(prompts, log_probs, ref_log_probs, reward_score, action_mask)
    fixed_rewards = compute_rewards_fixed(prompts, log_probs, ref_log_probs, reward_score, action_mask)

    start = len(prompts[0]) - 1
    current_advantages, current_returns = get_advantages_and_returns(values, current_rewards, start)
    fixed_advantages, fixed_returns = get_advantages_and_returns(values, fixed_rewards, start)

    current_mask = [action_mask[0][start:]]
    current_loss = actor_loss_fn([log_probs[0][start:]], [ref_log_probs[0][start:]], current_advantages, current_mask)
    fixed_loss = actor_loss_fn([log_probs[0][start:]], [ref_log_probs[0][start:]], fixed_advantages, current_mask)

    result = {
        "seq": seq,
        "attention_mask": attention_mask,
        "action_mask": action_mask,
        "start": start,
        "current_end_index": ends[0],
        "current_reward_target_index": ends[0] - 1,
        "current_reward_target_mask_value": current_mask[0][-1],
        "eos_index_in_rewards": start + sum(action_mask[0][start:]) - 1,
        "eos_mask_value": current_mask[0][-2],
        "current_rewards": current_rewards,
        "fixed_rewards": fixed_rewards,
        "current_advantages": current_advantages,
        "fixed_advantages": fixed_advantages,
        "current_returns": current_returns,
        "fixed_returns": fixed_returns,
        "current_actor_loss": current_loss,
        "fixed_actor_loss": fixed_loss,
        "loss_delta": current_loss - fixed_loss,
        "bug_summary": (
            "The reward model reward is written to the padded position "
            "instead of the EOS action, so the terminal reward is masked out "
            "by actor_loss_fn's action_mask[:, start:] slice."
        ),
    }

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
