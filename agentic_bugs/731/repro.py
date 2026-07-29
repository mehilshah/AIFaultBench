#!/usr/bin/env python3
"""Offline reproduction for CAMEL Minimax's incorrect default endpoint."""

import os

# Reproduce the report's "not explicitly configured" case without touching a
# real API.  The non-empty key only satisfies CAMEL's constructor guard.
os.environ.pop("MINIMAX_API_BASE_URL", None)
os.environ["MINIMAX_API_KEY"] = "offline-test-key"

from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType


class OfflineClient:
    """Inert OpenAI-compatible client; no completion can reach the network."""


model = ModelFactory.create(
    model_platform=ModelPlatformType.MINIMAX,
    model_type=ModelType.MINIMAX_M2_7,
    client=OfflineClient(),
    async_client=OfflineClient(),
)

expected = "https://api.minimax.io/v1"
observed = model._url
print(f"OBSERVED_MINIMAX_DEFAULT_URL={observed}")
assert observed == expected, (
    "BUG: an unset MINIMAX_API_BASE_URL selected "
    f"{observed!r}; international users require {expected!r}"
)
