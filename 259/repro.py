import os
import sys

import numpy as np
import pandas as pd


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "codebase"))

from sdv.metadata import Metadata
from sdv.sequential import PARSynthesizer


def main():
    np.random.seed(0)

    data = pd.DataFrame(
        {
            "sequence_key": [f"sequence-{int(i / 5)}" for i in range(100)],
            "numerical_col": np.random.randint(low=0, high=100, size=100),
            "categorical_col": np.random.choice(["A", "B", "C"], size=100),
            "all_null_col": [np.nan] * 100,
        }
    )

    metadata = Metadata.load_from_dict(
        {
            "tables": {
                "table": {
                    "columns": {
                        "sequence_key": {"sdtype": "id"},
                        "numerical_col": {"sdtype": "numerical"},
                        "categorical_col": {"sdtype": "categorical"},
                        "all_null_col": {"sdtype": "numerical"},
                    },
                    "sequence_key": "sequence_key",
                }
            }
        }
    )

    synthesizer = PARSynthesizer(metadata, epochs=1)
    synthesizer.fit(data)
    print("fit ok")
    synthesizer.sample(num_sequences=2)


if __name__ == "__main__":
    main()

