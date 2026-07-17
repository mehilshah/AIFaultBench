# Bug 004

This folder reproduces the `MixupAndCutmix._sample_from_beta` bug reported in:
`https://github.com/tensorflow/models/issues/13490`

The local buggy implementation is in:
`codebase/official/vision/ops/augment.py`

Reproduction flow:
1. Create the virtualenv and install deps with `./setup_env.sh`
2. Run `./run_repro.sh`
3. Inspect `repro_stdout.log` and `repro_stderr.log`

What the repro checks:
1. It verifies the local source still contains the buggy gamma sampling lines.
2. It samples from the buggy implementation at `alpha=0.2`.
3. It compares the output to `numpy.random.beta(0.2, 0.2, ...)` and a uniform reference.
4. It confirms the buggy output is much closer to `Beta(1, 1)` than to the intended beta distribution.

Generated artifacts:
1. `repro.py`
2. `requirements.txt`
3. `setup_env.sh`
4. `run_repro.sh`
5. `Dockerfile`
6. `manifest.json`
7. `reproduction.json`
8. `repro_stdout.log`
9. `repro_stderr.log`
