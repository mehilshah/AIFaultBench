# Reproduction Trajectory — Bug 075: DeepSpeedExamples

- **Bug report:** [https://github.com/deepspeedai/DeepSpeedExamples/issues/847](https://github.com/deepspeedai/DeepSpeedExamples/issues/847)
- **Repository:** deepspeedai/DeepSpeedExamples @ `ff9a0234cf22dd9af03c5c7aa8037fb9143adca6`
- **Outcome:**  Not reproduced on the reference machine

## How the bug was reproduced

1. Created a local virtual environment and installed the pinned reproduction dependencies from requirements.txt.
2. Ran ./repro.py through ./run_repro.sh.
3. Observed the terminal output BUG_NOT_REPRODUCED instead of the reported ParquetConfig token failure.

## Observed behavior

- On Python 3.11.15 with datasets==2.16.1, huggingface-hub==0.20.3, pyarrow==14.0.2, and numpy==1.26.4, the repro script loaded wikitext with token='dummy-token' successfully.
- The same script also loaded a local parquet file with token='dummy-token' successfully, and no ParquetConfig.__init__ TypeError was raised.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
./run_repro.sh
```

## Why it does not reproduce on the reference machine

The reported ParquetConfig.__init__() unexpected keyword argument 'token' error does not reproduce with the closest compatible package set available in this folder; both the wikitext and parquet token-loading paths succeed.
