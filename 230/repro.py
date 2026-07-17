from __future__ import annotations

import json
import time

import optuna


def objective(trial: optuna.Trial) -> float:
    x = trial.suggest_int("x", 0, 1)
    time.sleep(x)
    y = trial.suggest_int("y", 0, 1)
    return float(x + y)


def main() -> None:
    sampler = optuna.samplers.BruteForceSampler(seed=42)
    study = optuna.create_study(sampler=sampler)
    study.optimize(objective, n_jobs=2)

    trials = [
        {
            "number": t.number,
            "state": t.state.name,
            "params": t.params,
            "value": t.value,
        }
        for t in study.trials
    ]
    expected = {
        frozenset({"x": 0, "y": 0}.items()),
        frozenset({"x": 0, "y": 1}.items()),
        frozenset({"x": 1, "y": 0}.items()),
        frozenset({"x": 1, "y": 1}.items()),
    }
    observed = {frozenset(t["params"].items()) for t in trials}

    print(json.dumps({"trial_count": len(trials), "trials": trials}, indent=2, sort_keys=True))

    if observed != expected:
        missing = sorted(
            [dict(items) for items in expected - observed],
            key=lambda d: (d.get("x", -1), d.get("y", -1)),
        )
        raise AssertionError(f"Incomplete brute-force coverage: missing={missing}")


if __name__ == "__main__":
    main()
