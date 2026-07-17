# Reproduction Trajectory — Bug 608: transformers

- **Bug report:** [https://github.com/huggingface/transformers/issues/46710](https://github.com/huggingface/transformers/issues/46710)
- **Repository:** huggingface/transformers @ `b4b5244c9c7cdb80d0aaafdb8f35244612788532`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Create the isolated environment with `bash setup_env.sh`.
2. Run the repro with `bash run_repro.sh`.
3. Inspect `repro_stdout.log` and `repro_stderr.log` for the failing round-trip comparisons.

## Observed behavior

- In a clean virtualenv with transformers 5.9.0, AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Llama-8B") loads LlamaTokenizer and round-tripping "What is 1+1? Answer briefly." decodes to "Whatis1+1?Answerbriefly." instead of preserving spaces.
- The chat-template prompt for the same model also round-trips incorrectly: "<｜begin▁of▁sentence｜><｜User｜>What is 1+1? Answer briefly.<｜Assistant｜><think>\n" decodes to "<｜begin of sentence｜><｜User｜>Whatis1+1?Answerbriefly.<｜Assistant｜><think>".

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
