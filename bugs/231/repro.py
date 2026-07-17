#!/usr/bin/env python3
"""Reproduce Optuna GridSampler duplicating an enqueued grid point."""

from __future__ import annotations

from collections import Counter

import optuna


def main() -> None:
    search_space = {f"c{i}": [str(i) for i in range(2)] for i in range(2)}
    target_params = {k: v[0] for k, v in search_space.items()}

    def objective(trial: optuna.Trial) -> float:
        for key, values in search_space.items():
            trial.suggest_categorical(key, values)
        return 0.0

    study = optuna.create_study(
        sampler=optuna.samplers.GridSampler(search_space=search_space)
    )
    study.enqueue_trial(target_params)
    study.optimize(objective)

    params = [trial.params for trial in study.trials]
    counts = Counter(tuple(sorted(p.items())) for p in params)
    duplicated = counts[tuple(sorted(target_params.items()))]

    print(f"trial_count={len(study.trials)}")
    for trial in study.trials:
        print(f"trial_{trial.number}={trial.params} attrs={trial.system_attrs}")
    print(f"target_occurrences={duplicated}")

    expected_trial_count = 5
    expected_target_occurrences = 2
    if len(study.trials) != expected_trial_count or duplicated != expected_target_occurrences:
        raise SystemExit(
            "BUG NOT REPRODUCED: expected the enqueued grid point to appear twice "
            f"across {expected_trial_count} total trials."
        )

    print("BUG REPRODUCED: enqueued grid point was evaluated twice.")


if __name__ == "__main__":
    main()
