import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist


def main() -> None:
    value = dist.Beta(1.0, 8.0).log_prob(0.0)
    expected = jnp.log(8.0)

    print(f"numpyro={numpyro.__version__}")
    print(f"jax={jax.__version__}")
    print(f"log_prob={value}")
    print(f"expected={expected}")
    print(f"isnan={jnp.isnan(value)}")

    assert not jnp.isnan(value), "Beta(1.0, 8.0).log_prob(0.0) returned nan"
    assert jnp.isclose(value, expected), f"expected {expected}, got {value}"


if __name__ == "__main__":
    main()
