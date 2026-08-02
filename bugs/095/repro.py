#!/usr/bin/env python3
class GaussianDiffusion:
    def ddim_sample(self, shape, return_all_timesteps=False):
        # This mirrors the failing call site in
        # denoising_diffusion_pytorch/denoising_diffusion_pytorch.py.
        img = object()
        time_cond = object()
        self_cond = None
        return self.model_predictions(
            img,
            time_cond,
            self_cond,
            clip_x_start=True,
            rederive_pred_noise=True,
        )


class LearnedGaussianDiffusion(GaussianDiffusion):
    def model_predictions(self, x, t, clip_x_start=False):
        return x, t, clip_x_start


def main():
    LearnedGaussianDiffusion().ddim_sample((1, 1, 1, 1))


if __name__ == "__main__":
    main()
