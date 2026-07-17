from __future__ import annotations

import os
import sys
from typing import Final, List, Optional, Tuple

ROOT = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.join(ROOT, "codebase")
if CODEBASE not in sys.path:
    sys.path.insert(0, CODEBASE)

import torch
from torch import Tensor

from torch_geometric.inspector import Inspector
from torch_geometric.nn import SAGEConv
from torch_geometric.utils import coalesce, sort_edge_index


def main() -> int:
    inspector = Inspector(SAGEConv)
    observed = inspector.type_repr(Final[Optional[Tensor]])
    expected = "typing.Final[Optional[Tensor]]"
    print(f"type_repr(Final[Optional[Tensor]]) = {observed}")
    print(f"expected = {expected}")

    @torch.jit.script
    def coalesce_optional(
        edge_index: Tensor,
        edge_attr: Optional[Tensor],
    ) -> Tuple[Tensor, Optional[Tensor]]:
        return coalesce(edge_index, edge_attr)

    @torch.jit.script
    def coalesce_list(
        edge_index: Tensor,
        edge_attr: List[Tensor],
    ) -> Tuple[Tensor, List[Tensor]]:
        return coalesce(edge_index, edge_attr)

    @torch.jit.script
    def sort_optional(
        edge_index: Tensor,
        edge_attr: Optional[Tensor],
    ) -> Tuple[Tensor, Optional[Tensor]]:
        return sort_edge_index(edge_index, edge_attr)

    edge_index = torch.tensor([[2, 1, 1, 0], [1, 2, 0, 1]])
    edge_attr = torch.tensor([[1], [2], [3], [4]])

    out1 = coalesce_optional(edge_index, None)
    out2 = coalesce_optional(edge_index, edge_attr)
    out3 = coalesce_list(edge_index, [edge_attr, edge_attr.view(-1)])
    out4 = sort_optional(edge_index, None)
    out5 = sort_optional(edge_index, edge_attr)

    print(f"coalesce_optional(None) -> {out1[0].tolist()}, {out1[1]}")
    print(f"coalesce_optional(Tensor) -> {out2[0].tolist()}, {out2[1].tolist()}")
    print(f"coalesce_list -> {out3[0].tolist()}, {[x.tolist() for x in out3[1]]}")
    print(f"sort_optional(None) -> {out4[0].tolist()}, {out4[1]}")
    print(f"sort_optional(Tensor) -> {out5[0].tolist()}, {out5[1].tolist()}")

    if observed != expected:
        print("RESULT: REPRODUCIBLE")
        return 1

    print("RESULT: NOT_REPRODUCIBLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
