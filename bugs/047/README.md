# Bug 047

This folder reproduces the MMS ASR output-order bug from fairseq issue
`facebookresearch/fairseq#5152`.

What the repro does:
- Replays the exact `reorder_decode` logic from `codebase/examples/mms/asr/infer/mms_infer.py`
- Feeds it the misordered hypothesis sequence reported in `bug_report.txt`
- Shows that the final `Input:` / `Output:` pairing is incorrect

Files of interest:
- [`bug_report.txt`](./bug_report.txt)
- [`codebase/examples/mms/asr/infer/mms_infer.py`](./codebase/examples/mms/asr/infer/mms_infer.py)
- [`repro.py`](./repro.py)
- [`fixtures/hypo.word`](./fixtures/hypo.word)

Run:
```bash
bash run_repro.sh
```

Expected outcome:
- `reproducible: true`
- The printed mapping shows the observed transcript order does not match the
  expected audio order.
