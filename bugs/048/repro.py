#!/usr/bin/env python3
"""Self-contained reproduction of the MMS forced-alignment concat bug.

This mirrors the sliding-window logic in
`examples/mms/data_prep/align_and_segment.py` and reproduces the failure at
the emission concatenation step when window outputs differ in time length.
"""

from dataclasses import dataclass


SAMPLING_FREQ = 16000
EMISSION_INTERVAL = 30
STRIDE_MSEC = 20
TOTAL_DURATION_SEC = 63.0


def time_to_frame(time_sec: float) -> int:
    frames_per_sec = 1000 / STRIDE_MSEC
    return int(time_sec * frames_per_sec)


@dataclass(frozen=True)
class FakeEmission:
    time_steps: int
    feature_dim: int = 31


def fake_model_output_length(input_duration_sec: float) -> int:
    # Approximate a 20 ms stride and keep the reported off-by-one behavior.
    return max(1, int(input_duration_sec * 1000 / STRIDE_MSEC) - 1)


def fake_cat(tensors, dim):
    if not tensors:
        raise RuntimeError("torch.cat received an empty list of tensors")

    expected = tensors[0].time_steps
    for idx, tensor in enumerate(tensors[1:], start=1):
        if tensor.time_steps != expected:
            raise RuntimeError(
                f"Sizes of tensors must match except in dimension {dim}. "
                f"Expected size {expected} but got size {tensor.time_steps} "
                f"for tensor number {idx} in the list."
            )

    total = sum(t.time_steps for t in tensors)
    return FakeEmission(total, tensors[0].feature_dim)


def generate_emissions():
    emissions_arr = []
    i = 0
    while i < TOTAL_DURATION_SEC:
        segment_start_time, segment_end_time = i, i + EMISSION_INTERVAL

        context = EMISSION_INTERVAL * 0.1
        input_start_time = max(segment_start_time - context, 0)
        input_end_time = min(segment_end_time + context, TOTAL_DURATION_SEC)

        input_duration = input_end_time - input_start_time
        emission_steps = fake_model_output_length(input_duration)

        # In the original code, the slice is taken from the model output and the
        # per-window tensors are then concatenated along dim=1.
        emissions_arr.append(FakeEmission(emission_steps))
        print(
            f"window {i:>2.0f}-{segment_end_time:>2.0f}s "
            f"input={input_duration:>4.1f}s -> {emission_steps} frames"
        )
        i += EMISSION_INTERVAL

    return fake_cat(emissions_arr, dim=1)


def main():
    print("Using torch version: simulated")
    print("Using torchaudio version: simulated")
    print("Using device: cpu")
    print(f"Simulated sample rate: {SAMPLING_FREQ}")
    generate_emissions()


if __name__ == "__main__":
    main()
