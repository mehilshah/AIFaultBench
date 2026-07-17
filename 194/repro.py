import equinox as eqx
import jax
import jax.numpy as jnp


def foo(x):
    return x * 2.0


def main():
    x = jnp.arange(24).reshape((2, 3, 4))
    y = jax.vmap(foo, out_axes=-1)(x)
    z = eqx.filter_vmap(foo, out_axes=-1)(x)

    print(f"jax: {y.shape} eqx: {z.shape}")
    print(f"jax version: {jax.__version__}")
    print(f"equinox version: {eqx.__version__}")

    if z.shape != y.shape:
        print("BUG REPRODUCED: wrong out_axes arrangement")
        raise AssertionError(
            f"wrong out_axes arrangement: expected {y.shape}, got {z.shape}"
        )


if __name__ == "__main__":
    main()
