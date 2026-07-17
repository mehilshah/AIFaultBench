#!/usr/bin/env python3
"""Minimal reproduction for GaussianCopulaSynthesizer.get_learned_distributions."""

from __future__ import annotations

import os
import sys
import traceback
import types


def _install_stub_modules() -> None:
    """Stub unrelated package-level imports that are not needed for this repro."""
    ctgan = types.ModuleType('ctgan')

    class _DummyModel:
        pass

    ctgan.CTGAN = _DummyModel
    ctgan.TVAE = _DummyModel
    sys.modules['ctgan'] = ctgan

    deepecho = types.ModuleType('deepecho')
    deepecho.__path__ = []  # Mark as a package so deepecho.sequences can be imported.
    deepecho.PARModel = _DummyModel
    sys.modules['deepecho'] = deepecho

    deepecho_sequences = types.ModuleType('deepecho.sequences')
    deepecho_sequences.assemble_sequences = lambda *args, **kwargs: None
    sys.modules['deepecho.sequences'] = deepecho_sequences

    sdmetrics = types.ModuleType('sdmetrics')
    sdmetrics.__path__ = []
    sdmetrics_single_table = types.ModuleType('sdmetrics.single_table')
    sdmetrics_multi_table = types.ModuleType('sdmetrics.multi_table')
    sdmetrics_timeseries = types.ModuleType('sdmetrics.timeseries')
    sdmetrics_visualization = types.ModuleType('sdmetrics.visualization')

    class PlotConfig:
        DATACEBO_DARK = '#000000'
        DATACEBO_GREEN = '#00ff00'
        BACKGROUND_COLOR = '#ffffff'
        FONT_SIZE = 12

    sdmetrics_visualization.PlotConfig = PlotConfig
    sdmetrics.single_table = sdmetrics_single_table
    sdmetrics.multi_table = sdmetrics_multi_table
    sdmetrics.timeseries = sdmetrics_timeseries
    sdmetrics.visualization = sdmetrics_visualization
    sys.modules['sdmetrics'] = sdmetrics
    sys.modules['sdmetrics.single_table'] = sdmetrics_single_table
    sys.modules['sdmetrics.multi_table'] = sdmetrics_multi_table
    sys.modules['sdmetrics.timeseries'] = sdmetrics_timeseries
    sys.modules['sdmetrics.visualization'] = sdmetrics_visualization


def main() -> int:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    codebase_path = os.path.join(repo_root, 'codebase')
    if codebase_path not in sys.path:
        sys.path.insert(0, codebase_path)

    _install_stub_modules()

    import pandas as pd
    from sdv.metadata import Metadata
    from sdv.single_table import GaussianCopulaSynthesizer

    metadata = Metadata().load_from_dict(
        {
            'tables': {
                'table1': {
                    'columns': {
                        'col_1': {'sdtype': 'id'},
                        'col_2': {'sdtype': 'credit_card_number'},
                    }
                }
            }
        }
    )
    data = pd.DataFrame({'col_1': range(100), 'col_2': range(100)})

    synthesizer = GaussianCopulaSynthesizer(metadata, default_distribution='beta')
    print(f'before_fit _fitted={synthesizer._fitted} _model={synthesizer._model}')
    synthesizer.fit(data)
    processed_columns = list(synthesizer._data_processor.transform(data).columns)
    print(f'after_fit _fitted={synthesizer._fitted} _model={synthesizer._model}')
    print(f'processed_columns={processed_columns}')

    try:
        result = synthesizer.get_learned_distributions()
    except Exception as exc:  # noqa: BLE001 - we want the exact failure for the repro.
        print(f'get_learned_distributions raised {type(exc).__name__}: {exc}', file=sys.stderr)
        traceback.print_exc()
        return 1

    print(f'get_learned_distributions returned: {result}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
