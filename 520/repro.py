import numpy as np
import jax
import jax.numpy as jnp


def program(x):
    return jnp.sqrt(jnp.abs(jnp.square(jax.nn.relu(x))))


def main():
    x = jnp.array([3.4028235e+38], dtype=jnp.float32)

    jit_result = np.asarray(jax.jit(jax.vmap(program))(x))
    eager_result = np.asarray(jax.vmap(program)(x))

    print("jit(vmap(f))(x):", jit_result)
    print("    vmap(f)(x): ", eager_result)

    np.testing.assert_allclose(
        jit_result,
        eager_result,
        rtol=1e-5,
        atol=1e-5,
        err_msg="jit(vmap(f)) != vmap(f) for relu -> square -> sqrt_abs",
    )


if __name__ == "__main__":
    main()

