# Reproduction Trajectory — Bug 730: semantic-kernel

- **Bug report:** [https://github.com/microsoft/semantic-kernel/issues/13148](https://github.com/microsoft/semantic-kernel/issues/13148)
- **Repository:** microsoft/semantic-kernel @ `28ea2f4df872e8fd03ef0792ebc9e1989b4be0ee`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` to clone the repository and check out the pinned commit.
2. Ran `bash setup_env.sh`, which created `.venv`, provisioned an isolated .NET 8.0.129 SDK, and restored the connector project dependencies.
3. Ran `bash run_repro.sh`. Its minimal C# harness uses the report's `Kernel.CreateBuilder().AddHuggingFaceEmbeddingGenerator(...)` path with an in-process `HttpMessageHandler` that deterministically returns HTTP 404.

## Observed behavior

- The connector sent the embedding request to `https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2`, the obsolete host identified in the report.
- The stubbed 404 was translated to `HttpOperationException`, and the repro printed `OBSERVED_BUG: HttpOperationException 404 after request to https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2` before exiting 1.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
