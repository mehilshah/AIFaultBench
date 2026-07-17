# Reproduction Trajectory — Bug 299: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/47277](https://github.com/huggingface/transformers/issues/47277)
- **Repository:** huggingface/transformers @ `63f32a8782cb70da3365acab16f2b67947737985`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Installed local Transformers tree without dependencies.
2. tokenizers==0.23.0 was unavailable on this package index, so the Linux wheel fallback was tried instead.
3. Installed tokenizers==0.23.1 from the Linux wheel path.
4. Verified installed package metadata without importing the library.

## Observed behavior

- Local installation succeeded and tokenizers was resolved through the normal Linux wheel path; the reported `pthread_cond_clockwait` / `esaxx-rs` Android build failure did not occur.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported failure depends on the Android/Termux aarch64 build stack with clang++ and libc++ headers; this folder is running on Linux x86_64 without that toolchain.
