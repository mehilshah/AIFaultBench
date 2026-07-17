#!/usr/bin/env python
"""Minimal repro for float categorical columns in PARSynthesizer."""

from __future__ import annotations

from sdv.datasets.demo import download_demo
from sdv.evaluation.single_table import run_diagnostic
from sdv.sequential import PARSynthesizer


def main() -> None:
    data, metadata = download_demo('sequential', 'nasdaq100_2019')
    data['category'] = [100.0 if i % 2 == 0 else 50.0 for i in data.index]
    metadata.add_column('category', sdtype='categorical')

    synth = PARSynthesizer(metadata)
    synth.fit(data)
    sampled = synth.sample(2)

    report = run_diagnostic(data, sampled, metadata, verbose=False)
    validity = report.get_details('Data Validity')
    category_score = float(validity.loc[validity['Column'] == 'category', 'Score'].iloc[0])

    print(f'data_rows={len(data)}')
    print(f'sampled_shape={sampled.shape}')
    print(f'sampled_category_dtype={sampled["category"].dtype}')
    print(f'sampled_category_head={sampled["category"].head(20).tolist()}')
    print(f'diagnostic_score={report.get_score()}')
    print(f'category_adherence_score={category_score}')
    print(validity.to_string(index=False))


if __name__ == '__main__':
    main()
