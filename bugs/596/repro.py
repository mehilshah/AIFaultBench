from __future__ import annotations

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR / "codebase" / "src"))

import torch
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler


def main() -> int:
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is required for this reproduction.")

    torch.manual_seed(0)
    print(f"torch={torch.__version__}")
    print(f"cuda_device={torch.cuda.get_device_name(0)}")

    scheduler = UniPCMultistepScheduler(
        prediction_type="flow_prediction",
        use_flow_sigmas=True,
        flow_shift=3.0,
        solver_order=2,
    )
    scheduler.set_timesteps(3, device="cuda")
    print(f"timesteps={scheduler.timesteps.tolist()}")

    sample = torch.zeros((1, 4), device="cuda")
    model_output = torch.zeros_like(sample)

    for step_index, timestep in enumerate(scheduler.timesteps, start=1):
        print(f"running_step={step_index}, timestep={int(timestep)}")
        sample = scheduler.step(model_output, timestep, sample).prev_sample
        print(f"step_{step_index}_device={sample.device}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
