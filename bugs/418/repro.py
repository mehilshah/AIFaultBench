#!/usr/bin/env python3

import json

import torch
from torch_geometric.nn.conv import TransformerConv


def main() -> None:
    layer = TransformerConv(8, 4, bias=False)

    observed = {
        "lin_key_bias_is_none": layer.lin_key.bias is None,
        "lin_query_bias_is_none": layer.lin_query.bias is None,
        "lin_value_bias_is_none": layer.lin_value.bias is None,
        "lin_skip_bias_is_none": layer.lin_skip.bias is None,
    }

    print(json.dumps(
        {
            "torch_version": torch.__version__,
            "layer": "TransformerConv(8, 4, bias=False)",
            "observed": observed,
        },
        indent=2,
        sort_keys=True,
    ))

    expected = all(observed.values())
    if not expected:
        raise AssertionError(
            "bias=False is not respected by TransformerConv: "
            "lin_key, lin_query, and lin_value still have bias parameters"
        )


if __name__ == "__main__":
    main()
