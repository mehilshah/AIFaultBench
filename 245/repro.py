import warnings

warnings.filterwarnings("error", category=DeprecationWarning)

import jax

print(f"jax=={jax.__version__}")
print("importing numpyro")
import numpyro

print(f"numpyro=={numpyro.__version__}")
