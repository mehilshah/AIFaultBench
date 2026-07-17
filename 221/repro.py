#!/usr/bin/env python3
"""Minimal reproduction for torchio Pad minimum-padding behavior."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'codebase' / 'src'))

import torchio as tio  # noqa: E402


def border_voxels(volume: np.ndarray) -> np.ndarray:
    """Return all voxels on the outer border of a 3D volume."""
    assert volume.ndim == 3
    borders = [
        volume[0, :, :],
        volume[-1, :, :],
        volume[:, 0, :],
        volume[:, -1, :],
        volume[:, :, 0],
        volume[:, :, -1],
    ]
    return np.concatenate([border.ravel() for border in borders])


def main() -> int:
    # Distinct values across axes make the axis-wise padding behavior visible.
    data = np.array(
        [
            [[10, 11, 12], [13, 14, 15]],
            [[-2, 1, 3], [4, 5, 6]],
        ],
        dtype=np.float32,
    )
    image = tio.ScalarImage(tensor=data[None], affine=np.eye(4))
    subject = tio.Subject(img=image)
    padded = tio.Pad(1, padding_mode='minimum')(subject)
    padded_data = padded.img.data.numpy()[0]

    expected_fill = float(data.min())
    border = border_voxels(padded_data)
    reproducible = bool(np.any(border != expected_fill))

    evidence = (
        f'global_min={expected_fill}, '
        f'padded_shape={tuple(int(x) for x in padded_data.shape)}, '
        f'z0_face={padded_data[0].tolist()}, '
        f'y0_face={padded_data[:, 0, :].tolist()}, '
        f'x0_face={padded_data[:, :, 0].tolist()}'
    )

    result = {
        'reproducible': reproducible,
        'evidence': evidence,
        'steps': [
            'Create a synthetic 3D ScalarImage with a known global minimum.',
            "Apply tio.Pad(1, padding_mode='minimum').",
            'Inspect border voxels and compare them with the global minimum.',
        ],
        'blocking_reason': '' if reproducible else 'Could not observe the wrong padding behavior.',
        'reproduction_command': 'bash run_repro.sh',
    }
    (ROOT / 'reproduction.json').write_text(
        json.dumps(result, indent=2) + '\n',
        encoding='utf-8',
    )

    print('Reproducible:', reproducible)
    print(evidence)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
