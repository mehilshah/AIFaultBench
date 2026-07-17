#!/usr/bin/env python3
"""Minimal reproduction for the LTX2 connector layout regression.

The bug report describes a layout mismatch between the reference behavior and
the current diffusers implementation:

* valid prompt tokens should stay in order at the front of the sequence
* the register tile should be placed by absolute position in the tail
* the current implementation applies a masked write and then flips the whole
  sequence, which reverses both regions

This script uses the toy example from the issue body to make that mismatch
explicit.
"""

from __future__ import annotations

import torch


def reference_layout(hidden_states: torch.Tensor, attention_mask: torch.Tensor, registers: torch.Tensor) -> torch.Tensor:
    """Reference layout from the issue report.

    Preserve valid tokens in their original order and fill the tail with the
    register tile indexed by absolute position.
    """
    valid_tokens = hidden_states[attention_mask.bool()]
    valid_count = valid_tokens.shape[0]
    return torch.cat([valid_tokens, registers[valid_count:]], dim=0)


def current_layout(hidden_states: torch.Tensor, attention_mask: torch.Tensor, registers: torch.Tensor) -> torch.Tensor:
    """Current diffusers layout from `LTX2ConnectorTransformer1d.forward`.

    This mirrors the code in `codebase/src/diffusers/pipelines/ltx2/connectors.py`:

    * replace padded slots with tiled registers using a mask write
    * flip the full sequence along the sequence dimension
    """
    mask = attention_mask.unsqueeze(-1)
    registers_expanded = registers.unsqueeze(0).expand(hidden_states.shape[0], -1, -1)
    hidden_states = mask * hidden_states + (1 - mask) * registers_expanded
    return torch.flip(hidden_states, dims=[1])[0]


def main() -> None:
    seq_len = 8
    valid_len = 3

    tokens = torch.arange(1, valid_len + 1, dtype=torch.float32).unsqueeze(-1)
    registers = torch.arange(4, dtype=torch.float32).unsqueeze(-1).repeat(seq_len // 4, 1)

    hidden_states = torch.cat([torch.zeros(seq_len - valid_len, 1), tokens], dim=0).unsqueeze(0)
    attention_mask = torch.cat(
        [torch.zeros(seq_len - valid_len, dtype=torch.float32), torch.ones(valid_len, dtype=torch.float32)],
        dim=0,
    ).unsqueeze(0)

    reference = reference_layout(hidden_states[0], attention_mask[0], registers)
    current = current_layout(hidden_states, attention_mask, registers)

    print("reference:", reference.squeeze(-1).tolist())
    print("current:  ", current.squeeze(-1).tolist())

    # The bug is present when the current layout does not match the reference.
    assert torch.equal(
        reference, current
    ), "layout mismatch: current diffusers behavior reverses prompt tokens and registers"


if __name__ == "__main__":
    main()
