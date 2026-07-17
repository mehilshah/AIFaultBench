#!/usr/bin/env python3
from __future__ import annotations

import json
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RESULT_PATH = ROOT / "reproduction.json"


def build_repro():
    import torch
    import torch.nn as nn

    from torch_geometric.data import Data
    from torch_geometric.explain import Explainer, ExplainerAlgorithm, Explanation

    class DummyAlg(ExplainerAlgorithm):
        def forward(self, model, x, edge_index, *, target, index=None, **kwargs):
            return Explanation()

        def supports(self):
            return True

    class ToyModel(nn.Module):
        def forward(self, data):
            return data.x.sum(dim=-1, keepdim=True)

    data = Data(
        x=torch.tensor([[1.0, 2.0], [3.0, 4.0]]),
        edge_index=torch.tensor([[0, 1], [1, 0]]),
    )

    explainer = Explainer(
        model=ToyModel(),
        algorithm=DummyAlg(),
        explanation_type='model',
        model_config=dict(
            mode='binary_classification',
            task_level='graph',
            return_type='probs',
        ),
        node_mask_type='attributes',
        edge_mask_type=None,
    )

    explainer(data.x, data.edge_index, data=data)


def main() -> int:
    result = {
        "reproducible": False,
        "evidence": "",
        "steps": [
            "Create a Data object with x and edge_index.",
            "Define a model whose forward signature is forward(self, data).",
            "Wrap the model in Explainer and pass data=data alongside x and edge_index.",
            "Call explainer(data.x, data.edge_index, data=data).",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    try:
        build_repro()
        result["evidence"] = "The call unexpectedly succeeded in this environment."
        result["blocking_reason"] = "No exception was raised."
    except TypeError as exc:
        traceback.print_exc()
        message = str(exc)
        result["evidence"] = message
        if "multiple values for argument 'data'" in message:
            result["reproducible"] = True
        else:
            result["blocking_reason"] = f"Unexpected TypeError: {message}"
    except Exception as exc:  # pragma: no cover
        traceback.print_exc()
        result["evidence"] = f"{type(exc).__name__}: {exc}"
        result["blocking_reason"] = "A different exception prevented the target call."

    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["reproducible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
