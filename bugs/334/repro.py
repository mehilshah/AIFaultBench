import json

from accelerate import PartialState
from accelerate.utils import gather_object


def main() -> None:
    distributed_state = PartialState()

    prompts = [str(i) for i in range(4)]
    batch_size = 2
    tokenized_prompts = [prompts[i : i + batch_size] for i in range(0, len(prompts), batch_size)]

    completions_per_process = []
    with distributed_state.split_between_processes(tokenized_prompts, apply_padding=True) as batched_prompts:
        for batch in batched_prompts:
            generated_text = [f"{distributed_state.device}: {t}" for t in batch]
            completions_per_process.extend(generated_text)

    completions_gather = gather_object(completions_per_process)
    expected = ["cpu: 0", "cpu: 1", "cpu: 2", "cpu: 3"]
    if distributed_state.is_main_process:
        print(
            json.dumps(
                {
                    "gathered": completions_gather,
                    "expected": expected,
                    "matches_expected": completions_gather == expected,
                },
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
