# Reproduction Trajectory — Bug 047: fairseq

- **Bug report:** [https://github.com/facebookresearch/fairseq/issues/5152](https://github.com/facebookresearch/fairseq/issues/5152)
- **Repository:** facebookresearch/fairseq @ `25c20e6a5e781e4ef05e23642f21c091ba64872e`
- **Outcome:**  Reproduced

## How the bug was reproduced

1. Read `bug_report.txt` and the MMS wrapper in `codebase/examples/mms/asr/infer/mms_infer.py`.
2. Created fixtures from the reported audio list and misordered hypothesis sequence.
3. Ran `bash run_repro.sh` and verified the mismatched pairings in `repro_stdout.log`.

## Observed behavior

- Running `bash run_repro.sh` reproduces the ordering defect: 9 of 10 logged Input/Output pairings mismatch the expected transcripts, and the first audio file is paired with the transcript from the last item in the reported sequence.

Full output is captured in [`repro_stdout.log`](./repro_stdout.log) and [`repro_stderr.log`](./repro_stderr.log).

## Commands

```bash
bash setup_codebase.sh      # clone the repository at the buggy commit
bash run_repro.sh
```
