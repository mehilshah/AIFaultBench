# Reproduction Trajectory — Bug 747: langchain

- **Bug report:** [https://github.com/langchain-ai/langchain/issues/37723](https://github.com/langchain-ai/langchain/issues/37723)
- **Repository:** langchain-ai/langchain @ `84e3c795ec292cd32156f65c37c1445abb94b576`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Ran `bash setup_codebase.sh` and verified the checkout was at the supplied pinned commit.
2. Created `.venv` and installed the issue-era `openai==2.38.0` and `pydantic==2.13.4` dependencies along with editable `langchain-core` and `langchain-openai` from the checkout.
3. Constructed an OpenAI SDK `ParsedChatCompletion` containing an `IntentRecognitionOutput` Pydantic object, then supplied it through a local fake OpenAI response parser.
4. Invoked the public `ChatOpenAI.with_structured_output(IntentRecognitionOutput).invoke` path and captured every warning.
5. Ran the final `bash run_repro.sh`, capturing stdout and stderr.

## Observed behavior

- The structured-output call returned the expected `IntentRecognitionOutput(classification="billing")` and emitted no warning containing `field_name='parsed'`.
- Final stdout: `NOT REPRODUCED: structured output completed with no parsed-field serializer warning`.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```

## Why it does not reproduce on the reference machine

The source retains the `model_dump` call identified in the issue, but with the issue-reported OpenAI and Pydantic versions Pydantic honors the nested `exclude` for `parsed`; the reported serializer warning is therefore absent from the public structured-output invocation.
