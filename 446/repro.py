#!/usr/bin/env python3
"""Check whether the reported SDV financial demo ordering bug is reproducible."""

from __future__ import annotations

import sys

from sdv.datasets.demo import download_demo


def main() -> int:
    data, metadata = download_demo(modality='multi_table', dataset_name='financial')
    metadata_tables = metadata.to_dict()['tables']

    mismatches = []
    for table_name in sorted(data):
        table_columns = list(data[table_name].columns)
        metadata_columns = list(metadata_tables[table_name]['columns'].keys())
        same_order = table_columns == metadata_columns

        print(f'{table_name}: data_columns={table_columns}')
        print(f'{table_name}: metadata_columns={metadata_columns}')
        print(f'{table_name}: same_order={same_order}')

        if not same_order:
            mismatches.append((table_name, table_columns, metadata_columns))

    if mismatches:
        print('BUG_REPRODUCED')
        for table_name, table_columns, metadata_columns in mismatches:
            print(f'mismatch:{table_name}:{table_columns!r}:{metadata_columns!r}')
        return 1

    print('BUG_NOT_REPRODUCED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
