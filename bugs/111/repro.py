#!/usr/bin/env python3
"""Deterministic repro for PyGAD issue 335.

The bug report says integer genes initialized with init_range_low=0 can end up
below that lower bound after running the GA.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
CODEBASE = ROOT / "codebase"
sys.path.insert(0, str(CODEBASE))

import pygad  # noqa: E402


def fitness_func(ga_instance, solution, solution_idx):
    del ga_instance, solution_idx
    return np.sum(solution[0::2]) - np.sum(solution[1::2])


def main() -> int:
    ga_instance = pygad.GA(
        num_generations=50,
        num_parents_mating=10,
        fitness_func=fitness_func,
        sol_per_pop=100,
        num_genes=20,
        gene_type=int,
        init_range_low=0,
        init_range_high=2,
        parent_selection_type="sss",
        keep_parents=10,
        crossover_type="scattered",
        mutation_type="random",
        mutation_percent_genes=100 / 20,
        random_seed=0,
    )
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    min_gene = int(np.min(solution))
    max_gene = int(np.max(solution))

    print(f"pygad_version={getattr(pygad, '__version__', 'unknown')}")
    print(f"init_range_low=0 init_range_high=2")
    print(f"best_solution_index={solution_idx}")
    print(f"best_solution={solution}")
    print(f"best_solution_fitness={solution_fitness}")
    print(f"solution_min={min_gene} solution_max={max_gene}")

    if min_gene < 0:
        print("BUG_REPRODUCED: gene values fell below init_range_low=0")
        return 0

    raise AssertionError(
        "Expected a gene value below init_range_low=0, but all genes stayed non-negative."
    )


if __name__ == "__main__":
    raise SystemExit(main())
