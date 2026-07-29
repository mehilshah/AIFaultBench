# Reproduction Trajectory — Bug 701: pydantic-ai

- **Bug report:** [https://github.com/pydantic/pydantic-ai/issues/6286](https://github.com/pydantic/pydantic-ai/issues/6286)
- **Repository:** pydantic/pydantic-ai @ `d7e399521c1d1a7f617af88dfa8ef0a213382761`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Ran `bash setup_codebase.sh`, then verified and checked out the pinned commit in `codebase/`.
2. Created `.venv` and installed the pinned Python dependencies and editable `pydantic_graph` and `pydantic_ai_slim` packages from that checkout.
3. Constructed a `ModelRequest` containing a `NativeToolReturnPart`, serialized it with `ModelMessagesTypeAdapter.dump_json`, and validated the same JSON with `ModelMessagesTypeAdapter.validate_json`.
4. Ran `bash run_repro.sh`; the reproducer checked that the resulting validation error was specifically the missing `builtin-tool-return` discriminated-union tag and re-raised it.

## Observed behavior

- `run_repro.sh` exited with status 1 after printing `OBSERVED: ModelRequest NativeToolReturnPart round-trip raised union_tag_invalid`.
- Deserialization raised `pydantic_core._pydantic_core.ValidationError`: `Input tag 'builtin-tool-return' found using _model_request_part_discriminator() does not match any of the expected tags`, with error type `union_tag_invalid`.
- Serialization first emitted Pydantic warnings because `NativeToolReturnPart` matched none of the six declared `ModelRequestPart` members.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
