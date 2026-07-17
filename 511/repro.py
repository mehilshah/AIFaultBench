#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
RESULT_PATH = ROOT / "reproduction.json"

sys.path.insert(0, str(CODEBASE))

import torch  # noqa: E402
import torch_geometric  # noqa: E402
from torch_geometric.data import Data  # noqa: E402
from torch_geometric.sampler import NeighborSampler, NodeSamplerInput  # noqa: E402
from torch_geometric.sampler.neighbor_sampler import node_sample  # noqa: E402


def build_temporal_graph() -> Data:
    # Destination-sorted CSC ordering, but the source-node timestamps for the
    # neighborhood of dst=2 are intentionally unsorted: [5, 1, 9].
    edge_index = torch.tensor([
        [0, 1, 3, 2, 4],
        [2, 2, 2, 3, 3],
    ], dtype=torch.long)
    time = torch.tensor([5, 1, 9, 2, 7], dtype=torch.long)
    return Data(edge_index=edge_index, time=time, num_nodes=5)


def write_result(reproducible: bool, evidence: str, blocking_reason: str) -> None:
    payload = {
        "reproducible": reproducible,
        "evidence": evidence,
        "steps": [
            "Created a destination-sorted temporal graph whose neighborhood for dst=2 is not sorted by source timestamp.",
            "Instantiated NeighborSampler with time_attr='time' and is_sorted=True so the graph is not re-sorted by PyG.",
            "Called node_sample() and observed the backend RuntimeError from pyg-lib.",
        ],
        "blocking_reason": blocking_reason,
        "reproduction_command": "bash setup_env.sh && ./run_repro.sh",
    }
    RESULT_PATH.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    print(f"torch={torch.__version__}")
    print(f"torch_geometric={torch_geometric.__version__}")
    print(f"WITH_PYG_LIB={torch_geometric.typing.WITH_PYG_LIB}")
    print(
        "WITH_EDGE_TIME_NEIGHBOR_SAMPLE="
        f"{torch_geometric.typing.WITH_EDGE_TIME_NEIGHBOR_SAMPLE}"
    )

    data = build_temporal_graph()
    print(f"edge_index={data.edge_index.tolist()}")
    print(f"time={data.time.tolist()}")

    sampler = NeighborSampler(
        data=data,
        num_neighbors=[-1],
        disjoint=True,
        time_attr="time",
        is_sorted=True,
    )

    inputs = NodeSamplerInput(
        input_id=None,
        node=torch.tensor([2], dtype=torch.long),
        time=torch.tensor([10], dtype=torch.long),
    )

    try:
        out = node_sample(inputs, sampler._sample)
    except RuntimeError as exc:
        print("EXPECTED_RUNTIME_ERROR")
        print(str(exc))
        traceback.print_exc()

        reproducible = "Found invalid non-sorted temporal neighborhood" in str(
            exc
        )
        evidence = (
            "NeighborSampler on a destination-sorted temporal graph raised "
            f"RuntimeError: {exc}"
        )
        write_result(
            reproducible=reproducible,
            evidence=evidence,
            blocking_reason="" if reproducible else "Unexpected RuntimeError text.",
        )
        return 0 if reproducible else 1

    print("UNEXPECTED_SUCCESS")
    print(out)
    write_result(
        reproducible=False,
        evidence="Neighbor sampling completed without raising the reported RuntimeError.",
        blocking_reason="The temporal sampling backend did not fail in this environment.",
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
