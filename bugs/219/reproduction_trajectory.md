# Reproduction Trajectory — Bug 219: transformers

- **Bug report:** [https://github.com/tensorflow/datasets/issues/5310](https://github.com/tensorflow/datasets/issues/5310)
- **Repository:** tensorflow/datasets @ `49344e5`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Created a Python 3.10.13 environment with uv.
2. Installed tensorflow==2.15.0 and transformers==4.38.2.
3. Ran the reproduction snippet from the bug report with BertConfig(max_position_embeddings=2048).

## Observed behavior

- Using Python 3.10.13 with tensorflow==2.15.0 and transformers==4.38.2, TFBertModel.from_pretrained('bert-base-uncased', config=BertConfig(max_position_embeddings=2048)) fails. TensorFlow first raises InvalidArgumentError for a reshape mismatch, then transformers re-raises it as TypeError: InvalidArgumentError.__init__() missing 2 required positional arguments: 'op' and 'message'.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
