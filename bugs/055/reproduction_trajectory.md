# Reproduction Trajectory — Bug 055: keras-nlp

- **Bug report:** [https://github.com/keras-team/keras-io/issues/1703](https://github.com/keras-team/keras-io/issues/1703)
- **Repository:** keras-team/keras-io @ `789daa2f7a487771723de298aa3d0c7d87236d42`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created an isolated Python 3.11 virtualenv and installed tensorflow==2.15.0, keras==2.15.0, keras-nlp==0.6.4, tensorflow-text==2.15.0, and nltk==3.8.1.
2. Executed repro.py through run_repro.sh and observed three successful GreedySampler steps with output [1, 3, 3, 3].
3. Confirmed TensorFlow skipped GPU registration in this environment due missing CUDA runtime libraries.

## Observed behavior

- The pinned TensorFlow 2.15.0 / KerasNLP 0.6.4 environment installs successfully under Python 3.11.
- Running a minimal GreedySampler callback that returns logits, None hidden states, and an empty cache completes without a segfault.
- TensorFlow reports no usable GPU devices in this container because CUDA libraries cannot be dlopened, so the report's GPU-only crash path is not reachable here.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The environment cannot access the GPU execution path described in the report because TensorFlow 2.15.0 falls back to CPU after failing to dlopen CUDA libraries, and the sampler path completes normally on CPU.
