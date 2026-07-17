import torch


@torch.jit.script
def _capacity(gates: torch.Tensor, capacity_factor: torch.Tensor, min_capacity: torch.Tensor) -> torch.Tensor:
    num_tokens = gates.shape[0]
    num_experts = gates.shape[1]
    capacity = torch.ceil((num_tokens / num_experts) * capacity_factor).to(torch.int64)
    if capacity < min_capacity:
        capacity = min_capacity.to(torch.int64)
    return capacity


class TopKGate:
    pass
