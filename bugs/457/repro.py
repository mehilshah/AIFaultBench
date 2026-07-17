#!/usr/bin/env python3
"""Minimal repro for DensePose issue #334.

The historical DensePose evaluator hardcodes CUDA in:
`projects/DensePose/densepose/evaluation/densepose_coco_evaluation.py`
inside `findClosestVertsCse`:

    pixel_embeddings = embedding[:, py, px].t().to(device="cuda")

That means evaluation behavior depends on the runtime device instead of the
configured model device. This script exercises the exact control flow with
small fake tensors so the bug is observable without requiring the full model
zoo or dataset.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "codebase" / "projects" / "DensePose" / "densepose" / "evaluation" / "densepose_coco_evaluation.py"


class FakeMask:
    def __getitem__(self, _key):
        return self

    def __le__(self, other):
        return [True, False]


class FakeIndices:
    def __init__(self, values):
        self.values = list(values)

    def cpu(self):
        return self

    def __setitem__(self, key, value):
        # Keep the object mutable enough for the evaluator's post-processing.
        if isinstance(key, list):
            for i, flag in enumerate(key):
                if flag:
                    self.values[i] = value
        else:
            self.values[key] = value

    def as_list(self):
        return list(self.values)


class FakeDistanceMatrix:
    def argmin(self, dim=1):
        return FakeIndices([7, 11])


class FakeTensor:
    def __init__(self, device="cpu", cpu_only=True):
        self.device = device
        self.cpu_only = cpu_only

    def __getitem__(self, _key):
        return self

    def t(self):
        return self

    def to(self, device=None, **kwargs):
        target = device if device is not None else kwargs.get("device")
        if isinstance(target, str) and target.startswith("cuda") and self.cpu_only:
            raise RuntimeError("CUDA requested from a CPU-only tensor")
        self.device = target if target is not None else self.device
        return self


def squared_euclidean_distance_matrix(_pts1, _pts2):
    return FakeDistanceMatrix()


class FakeEmbedder:
    def __call__(self, _mesh_name):
        return FakeTensor(device="cpu", cpu_only=True)


class Evaluator:
    def __init__(self):
        self.embedder = FakeEmbedder()

    def findClosestVertsCse(self, embedding, py, px, mask, mesh_name):
        mesh_vertex_embeddings = self.embedder(mesh_name)
        pixel_embeddings = embedding[:, py, px].t().to(device="cuda")
        mask_vals = mask[py, px]
        edm = squared_euclidean_distance_matrix(pixel_embeddings, mesh_vertex_embeddings)
        vertex_indices = edm.argmin(dim=1).cpu()
        vertex_indices[mask_vals <= 0] = -1
        return vertex_indices

    def findClosestVertsCse_cpu_safe(self, embedding, py, px, mask, mesh_name):
        mesh_vertex_embeddings = self.embedder(mesh_name)
        pixel_embeddings = embedding[:, py, px].t().to(device=embedding.device)
        mask_vals = mask[py, px]
        edm = squared_euclidean_distance_matrix(pixel_embeddings, mesh_vertex_embeddings)
        vertex_indices = edm.argmin(dim=1).cpu()
        vertex_indices[mask_vals <= 0] = -1
        return vertex_indices


def main():
    source_text = SOURCE_FILE.read_text()
    hardcoded_line = 'pixel_embeddings = embedding[:, py, px].t().to(device="cuda")'
    if hardcoded_line not in source_text:
        raise RuntimeError(f"Expected source line not found in {SOURCE_FILE}")

    print(json.dumps({"source_file": str(SOURCE_FILE), "hardcoded_cuda_line_found": True}))
    print(hardcoded_line)

    evaluator = Evaluator()
    embedding = FakeTensor(device="cpu", cpu_only=True)
    mask = FakeMask()

    try:
        evaluator.findClosestVertsCse(embedding, 0, 0, mask, "mesh")
    except Exception as exc:
        print("current_impl", "failed", type(exc).__name__, str(exc))
    else:
        print("current_impl", "unexpectedly_passed")

    repaired = evaluator.findClosestVertsCse_cpu_safe(embedding, 0, 0, mask, "mesh")
    print("cpu_safe_reference", "passed", repaired.as_list())


if __name__ == "__main__":
    main()
