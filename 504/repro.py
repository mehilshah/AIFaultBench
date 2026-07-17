from torchrl.envs import StepCounter, TransformedEnv
from torchrl.testing.mocking_classes import NestedCountingEnv


def main() -> None:
    env = TransformedEnv(
        NestedCountingEnv(has_root_done=True, nest_done=True, max_steps=2),
        StepCounter(max_steps=2),
    )

    rollout = env.rollout(4)
    keys = set(rollout.keys(include_nested=True))

    print("done_keys:", env.done_keys)
    print("step_count_keys:", env.transform.step_count_keys)
    print("truncated_keys:", env.transform.truncated_keys)
    print("reset_keys:", env.transform.reset_keys)
    print("filtered_reset_keys:", env.transform.parent._filtered_reset_keys)
    print("top-level keys:", rollout.keys(include_nested=True))
    print("root step_count:", rollout["step_count"].squeeze(-1).tolist())
    print("root next truncated:", rollout["next", "truncated"].squeeze(-1).tolist())
    print("root next done:", rollout["next", "done"].squeeze(-1).tolist())
    print("nested next step_count exists:", ("next", "data", "step_count") in keys)
    print("nested next truncated exists:", ("next", "data", "truncated") in keys)
    print("nested next done exists:", ("next", "data", "done") in keys)

    assert ("next", "data", "step_count") in keys, (
        "StepCounter did not create a nested step_count key when a root done key was present"
    )
    assert ("next", "data", "truncated") in keys, (
        "StepCounter did not create a nested truncated key when a root done key was present"
    )


if __name__ == "__main__":
    main()
