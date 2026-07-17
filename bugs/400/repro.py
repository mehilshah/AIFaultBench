import jax.numpy as jnp
import numpyro.distributions as dist


def main() -> None:
    d = dist.Uniform(0.0, 5.0)
    log_prob = d.log_prob(7.0)
    density = jnp.exp(log_prob)
    print(f"log_prob={log_prob}")
    print(f"density={density}")
    assert float(density) == 0.0, "Expected zero density outside the support"


if __name__ == "__main__":
    main()
