from pathlib import Path
import sys
import traceback

import pandas as pd


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'codebase'))

from sdv.metadata import Metadata
from sdv.single_table import DayZSynthesizer


def main():
    data = pd.DataFrame()
    metadata = Metadata()

    print('running DayZSynthesizer.create_parameters with empty data and empty Metadata()')
    try:
        DayZSynthesizer.create_parameters(data, metadata)
    except Exception as exc:  # pragma: no cover - repro script
        print(f'exception_type={type(exc).__name__}')
        print(f'exception_message={exc}')
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()
