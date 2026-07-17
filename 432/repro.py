import sys
import traceback

import pgmpy


print(f"python={sys.version}")
print(f"pgmpy={pgmpy.__version__}")
print("importing pgmpy.estimators.CITests.chi_square, which is the lazy dependency used by")
print("torch_geometric.contrib.explain.PGMExplainer in codebase/torch_geometric/contrib/explain/pgm_explainer.py")

try:
    from pgmpy.estimators.CITests import chi_square  # noqa: F401
    print("import succeeded")
except Exception:
    traceback.print_exc()
    sys.exit(1)
