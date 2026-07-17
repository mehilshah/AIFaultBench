# Reproduction Trajectory — Bug 195: jaxtyping

- **Bug report:** [https://github.com/patrick-kidger/jaxtyping/issues/231](https://github.com/patrick-kidger/jaxtyping/issues/231)
- **Repository:** patrick-kidger/jaxtyping @ `c2f19db`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create a local virtual environment with bash setup_env.sh.
2. Run bash run_repro.sh to execute repro.py against the checked-out codebase.
3. Observe that the direct @beartype decorator on append_one(np.array([1, 2])) triggers jaxtyping.AnnotationError for the symbolic return axis dim+1.

## Observed behavior

- Running the minimal repro against the local codebase raises jaxtyping.AnnotationError.
- The error message is exactly: "Cannot process symbolic axis 'dim+1' as some axis names have not been processed. In practice you should usually only use symbolic axes in annotations for return types, referring only to axes annotated for arguments."
- The traceback shows the exception originates from codebase/jaxtyping/_array_types.py while checking the decorated function's return annotation.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
