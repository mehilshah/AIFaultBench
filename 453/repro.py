import json
import os
import random
import sys
import traceback


def _skip(msg: str) -> None:
    print(f"SKIP_ENV: {msg}", flush=True)
    sys.exit(0)


def env_int(key: str, default: int) -> int:
    value = os.environ.get(key, "").strip()
    if not value:
        return default
    try:
        return int(value)
    except Exception:
        return default


def env_bool(key: str, default: bool) -> bool:
    value = os.environ.get(key, "").strip().lower()
    if not value:
        return default
    return value in {"1", "true", "yes", "y", "on"}


def main() -> None:
    try:
        import torch
        import torch.distributed as dist
        import torch.nn as nn
        import torch.nn.functional as F
    except Exception as exc:
        _skip(f"missing torch/dist: {type(exc).__name__}: {exc}")

    try:
        import deepspeed
        from deepspeed import zero
    except Exception as exc:
        _skip(f"missing deepspeed: {type(exc).__name__}: {exc}")

    if not dist.is_available():
        _skip("torch.distributed not available")

    if not dist.is_initialized():
        dist.init_process_group(backend="nccl")

    rank = dist.get_rank()
    world = dist.get_world_size()
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    visible_gpus = max(torch.cuda.device_count(), 1)
    cuda_index = local_rank % visible_gpus
    torch.cuda.set_device(cuda_index)
    device = torch.device(f"cuda:{cuda_index}")
    os.environ["LOCAL_RANK"] = str(cuda_index)

    ds_config = os.environ.get("DEEPSPEED_CONFIG", "ds_config_zero3_stress.json")
    vocab = env_int("VOCAB", 32768)
    d_model = env_int("D_MODEL", 2048)
    iters = env_int("ITERS", 200)
    tile = env_int("TILE", 8)
    do_bwd = env_bool("DO_BWD", True)
    force_edit = env_bool("FORCE_GATHER_EDIT", True)

    try:
        cfg = json.load(open(ds_config, "r", encoding="utf-8"))
    except Exception as exc:
        _skip(f"cannot load {ds_config}: {type(exc).__name__}: {exc}")

    micro = int(cfg.get("train_micro_batch_size_per_gpu", 1))
    gas = int(cfg.get("gradient_accumulation_steps", 1))
    cfg["train_batch_size"] = micro * gas * world
    cfg.pop("optimizer", None)
    cfg["steps_per_print"] = max(int(cfg.get("steps_per_print", 0)), 1)

    if rank == 0:
        print(f"[rank0] dist ready world={world} device={device} visible_gpus={visible_gpus}", flush=True)

    class M(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.emb = nn.Embedding(vocab, d_model)
            self.l1 = nn.Linear(d_model, 4 * d_model, bias=False)
            self.l2 = nn.Linear(4 * d_model, d_model, bias=False)

        def forward(self, x):
            h = self.emb(x)
            h = self.l1(h)
            h = F.gelu(h)
            h = self.l2(h)
            return h.sum()

    model = M().to(device).train()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    try:
        if rank == 0:
            print("[rank0] before deepspeed.initialize", flush=True)
        engine, _, _, _ = deepspeed.initialize(
            model=model,
            model_parameters=[p for p in model.parameters() if p.requires_grad],
            optimizer=optimizer,
            config=cfg,
        )
    except Exception as exc:
        _skip(f"deepspeed.initialize failed: {type(exc).__name__}: {exc}")

    if rank == 0:
        print("[rank0] after deepspeed.initialize", flush=True)

    wrapped = getattr(engine, "module", engine)
    params = [wrapped.emb.weight, wrapped.l1.weight, wrapped.l2.weight]

    if rank == 0:
        print(
            f"[rank0] CONFIG world={world} device={device} visible_gpus={visible_gpus} "
            f"vocab={vocab} d_model={d_model} "
            f"iters={iters} tile={tile} do_bwd={do_bwd} force_edit={force_edit}",
            flush=True,
        )

    rnd = random.Random(2026 + rank)
    any_exc = None

    try:
        if rank == 0:
            print("[rank0] entering loop", flush=True)
        for i in range(1, iters + 1):
            x = torch.randint(0, vocab, (1, 8), device=device)

            with zero.GatheredParameters(params, modifier_rank=None):
                for p in params:
                    t = p.data
                    r = rnd.randrange(0, t.shape[0])
                    if t.ndim >= 2:
                        cmax = max(int(t.shape[1]) - tile, 1)
                        c0 = rnd.randrange(0, cmax)
                        _ = t[r, c0 : c0 + tile].sum().item()
                        if force_edit:
                            t[r, c0 : c0 + tile].add_(0.0)

            loss = engine(x)
            if do_bwd:
                engine.backward(loss)
                engine.step()
            else:
                engine.zero_grad()

            if rank == 0 and (i % 25 == 0 or i == iters):
                print(f"[rank0] step={i} ok", flush=True)

    except Exception as exc:
        any_exc = f"{type(exc).__name__}: {exc}"
        if rank == 0:
            print("[rank0] EXC TRACEBACK:", flush=True)
            traceback.print_exc()

    flag = torch.tensor([1 if any_exc else 0], device=device, dtype=torch.int32)
    dist.all_reduce(flag, op=dist.ReduceOp.MAX)
    hit = bool(int(flag.item()) == 1)

    if rank == 0:
        print(f"[rank0] RESULT hit={hit} exc={any_exc}", flush=True)

    decision = torch.tensor([1 if hit else 0], device=device, dtype=torch.int32)
    dist.broadcast(decision, src=0)
    dist.barrier()

    if int(decision.item()) == 1:
        if rank == 0:
            print("Test Passed", flush=True)
    else:
        if rank == 0:
            print("Test Failed", flush=True)

    dist.barrier()
    try:
        dist.destroy_process_group()
    except Exception:
        pass


if __name__ == "__main__":
    main()
