from __future__ import annotations

import json
import traceback
from functools import partial
from pathlib import Path

import jax
import flax
import numpyro
from flax import nnx
from numpyro.contrib.module import random_nnx_module


OUT_PATH = Path("reproduction.json")


class NNXModel(nnx.Module):
    def __init__(self, use_mutable: bool) -> None:
        self.linear = nnx.Linear(10, 1, rngs=nnx.Rngs(0))
        self.mutable = nnx.Variable(0) if use_mutable else None

    def __call__(self, x: jax.Array) -> jax.Array:
        return self.linear(x)


def model_fn(
    model: nnx.Module,
    x: jax.Array,
    y: jax.Array | None = None,
    use_deterministic: bool = False,
) -> jax.Array:
    random_model = random_nnx_module("model", model, numpyro.distributions.Normal(0, 1))
    x = random_model(x)
    with numpyro.plate("plate", size=x.shape[0]):
        x = numpyro.deterministic("x", x) if use_deterministic else x
        return numpyro.sample("obs", numpyro.distributions.Normal(x, 1.0).to_event(1), obs=y)


def run_case(label: str, use_mutable: bool, use_deterministic: bool) -> dict[str, object]:
    x = jax.random.uniform(jax.random.key(0), shape=(10, 10))
    y = jax.random.uniform(jax.random.key(0), shape=(10, 1))

    mcmc = numpyro.infer.MCMC(
        numpyro.infer.NUTS(
            partial(model_fn, NNXModel(use_mutable=use_mutable), use_deterministic=use_deterministic)
        ),
        num_warmup=10,
        num_samples=10,
    )

    try:
        with jax.check_tracer_leaks(True):
            mcmc.run(jax.random.key(0), x, y)
        return {"label": label, "ok": True}
    except Exception as exc:  # noqa: BLE001 - intentional repro capture
        traceback.print_exc()
        return {
            "label": label,
            "ok": False,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "traceback": traceback.format_exc(),
        }


def main() -> int:
    print(f"jax={jax.__version__}")
    print(f"numpyro={numpyro.__version__}")
    print(f"flax={flax.__version__}")

    control = run_case("control", use_mutable=False, use_deterministic=False)
    failing = run_case("mutable+deterministic", use_mutable=True, use_deterministic=True)

    reproducible = bool(control["ok"]) and (not failing["ok"]) and "Leaked trace" in str(
        failing.get("exception", "")
    )

    result = {
        "reproducible": bool(reproducible),
        "evidence": (
            "Control case without mutable state completed successfully; the mutable-state "
            "case with deterministic output failed with a JAX tracer leak during NUTS "
            "sampling."
        ),
        "steps": [
            "Install the pinned CPU JAX and Flax dependencies together with the local editable NumPyro checkout.",
            "Run the control MCMC case with NNX parameters but no mutable state.",
            "Run the mutable-state MCMC case with `numpyro.deterministic`, which raises `Leaked trace DynamicJaxprTrace`.",
        ],
        "blocking_reason": "",
        "reproduction_command": "bash run_repro.sh",
    }

    print("\nCONTROL RESULT:")
    print(json.dumps(control, indent=2, sort_keys=True))
    print("\nFAILING RESULT:")
    print(json.dumps(failing, indent=2, sort_keys=True))
    print("\nREPRO RESULT:")
    print(json.dumps(result, indent=2, sort_keys=True))

    OUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
