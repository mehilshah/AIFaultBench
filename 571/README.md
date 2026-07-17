# Bug 571

This folder contains a minimal reproduction for the reported zero `mAP@200` / `p@200` output while migrating a retrieval metric block to Lightning 2.x.

What the repro shows:
- A perfect sketch/gallery match still yields `AP = 0.0`.
- The reason is the score construction used in the report:
  - `distance = -1 * (1.0 - cosine_similarity(...))`
  - the positive pair gets score `0.0`
  - `torchmetrics.functional.retrieval_average_precision` masks non-positive scores before ranking
- `p@200` is also `0.0` in the posted snippet because the `pr` tensor is never populated.

Files:
- [`repro.py`](./repro.py)
- [`requirements.txt`](./requirements.txt)
- [`setup_env.sh`](./setup_env.sh)
- [`run_repro.sh`](./run_repro.sh)
- [`manifest.json`](./manifest.json)

Run locally:
```bash
./setup_env.sh
./run_repro.sh
```
