# Benchmark DL Bugs

A reproducibility benchmark of **640 real-world deep-learning bugs** mined from the issue
trackers of 104 popular ML/DL libraries (transformers, JAX, vLLM, DeepSpeed, diffusers,
PyTorch Lightning, TorchRL, PyG, detectron2, NumPyro, SDV, and more).

Every bug is packaged as a **self-contained, runnable reproduction**: a minimal script that
triggers the bug, the exact dependencies to install, a script that recreates the buggy
codebase at the offending commit, and a **reproduction trajectory** documenting how the bug
was reproduced and what was observed. Of the 640 bugs, **533 are verified reproducible**;
the remaining 107 are included with a documented reason they could not be reproduced on the
reference machine (e.g. multi-GPU-only code paths, hardware, or upstream fixes).

- **Bugs:** 640 &nbsp;·&nbsp; **Reproducible:** 533 &nbsp;·&nbsp; **Not reproducible:** 107
- **Libraries:** 104 &nbsp;·&nbsp; **Package size:** ~55 MB (codebases and environments are
  regenerated on demand, not shipped)

---

## 1. What's in the package

Each bug lives in its own numbered folder at the top level (`001/`, `002/`, …):

```
.
├── README.md                     # this file
├── index.csv                     # ← START HERE: canonical bug_id → report/commit/status map
├── index.json                    # same index, for programmatic use
└── <bug_id>/                     # one folder per bug: 001, 002, … (zero-padded)
```

### `index.csv` — the map

One row per bug; the single source of truth for setup and evaluation:

| column | meaning |
|--------|---------|
| `bug_id`           | folder name (e.g. `001`) |
| `library`          | ML/DL library the bug belongs to |
| `repository`       | GitHub `owner/repo` |
| `issue_url`        | the original bug report on GitHub |
| `commit`           | commit hash to check out for reproduction |
| `clone_url`        | git URL of the repository |
| `bug_report`       | path to the local bug-report text (e.g. `001/bug_report.txt`) |
| `codebase_present` | `true` if a codebase snapshot ships in-folder (rare); otherwise clone it |
| `reproducible`     | `true` / `false` — whether the bug was verified to reproduce |
| `blocking_reason`  | if not reproducible, why (empty otherwise) |
| `setup_command`    | commands to recreate codebase + environment |
| `run_command`      | command that triggers the bug |

### Each `<bug_id>/` folder

| file | purpose |
|------|---------|
| `bug_report.txt`            | the GitHub issue (title, date, URL, description, repro steps) |
| `repro.py`                  | minimal script that triggers the bug |
| `requirements.txt`          | bug-specific Python dependencies |
| `setup_codebase.sh`         | `git clone` + `git checkout <commit>` — recreates the codebase |
| `setup_env.sh`              | creates a local `.venv` and installs `requirements.txt` |
| `run_repro.sh`              | runs `setup_env.sh`, then `repro.py`, capturing stdout/stderr |
| `reproduction.json`         | structured record: `reproducible`, `steps`, `evidence`, `blocking_reason`, `reproduction_command` |
| `reproduction_trajectory.md`| human-readable narrative — **how the bug was reproduced** and what was observed |
| `repro_stdout.log` / `repro_stderr.log` | captured output from the reproduction run (evidence) |
| `README.md`, `manifest.json`| per-bug notes and metadata |

Some folders additionally carry a small helper module, config file, or vendored `codebase/`
where a plain clone was not sufficient — these are the only non-regenerable inputs and are
kept deliberately.

---

## 2. Reproducing a single bug

Reproduction uses a local Python **virtualenv** — no Docker required. Pick a bug id from
`index.csv`, then:

```bash
cd 001

# 1. Recreate the codebase at the buggy commit (not shipped with the dataset)
bash setup_codebase.sh

# 2. Build the environment and run the reproduction
bash run_repro.sh            # creates .venv, installs deps, runs repro.py

# 3. Inspect what happened
cat reproduction_trajectory.md   # the steps taken + expected observation
cat repro_stdout.log repro_stderr.log
```

`setup_env.sh` creates an isolated `.venv/` in the bug folder and installs
`requirements.txt`; `run_repro.sh` runs `repro.py` inside that venv. A reproducible bug fails
(raises the reported error, produces the wrong result, etc.) exactly as described in
`bug_report.txt`. The expected signal, the exact steps, and the evidence are documented in
`reproduction_trajectory.md` and `reproduction.json`.

> **Python versions.** Bugs pin their own dependency sets and may need a specific interpreter
> (e.g. `python3.10`); `setup_env.sh` selects it. Install the required interpreter if it is not
> already on `PATH`.
>
> **GPU bugs.** Some bugs require a GPU (or multiple GPUs); their `blocking_reason` in
> `index.csv` notes the hardware requirement. The 107 non-reproducible cases are mostly
> hardware- or platform-gated.

---

## 3. The reproduction trajectory

Each bug ships a `reproduction_trajectory.md` that records **how it was reproduced**:

- the **outcome** (reproduced / not reproduced on the reference machine),
- the ordered **steps** taken to trigger the bug,
- the **observed behavior** (with pointers to the captured logs),
- the exact **commands**, and
- for non-reproducible cases, **why** it does not reproduce here.

The same information in structured form lives in `reproduction.json`
(`steps`, `evidence`, `reproducible`, `blocking_reason`, `reproduction_command`), which is
convenient for programmatic analysis.

---

## 4. Running experiments across the whole benchmark

The benchmark is designed for evaluating automated tools — bug reproducers, program-repair /
APR systems, agents, fault localizers. Typical loop:

```bash
#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY' | while IFS= read -r bug_id; do
import csv
for r in csv.DictReader(open("index.csv")):
    if r["reproducible"] == "true":
        print(r["bug_id"])
PY
  ( cd "$bug_id" || exit 0
    bash setup_codebase.sh
    # --- invoke YOUR tool here, e.g. feed it bug_report.txt + codebase/ ---
    # your_tool --bug-report bug_report.txt --codebase codebase --repro repro.py
    bash run_repro.sh || true          # confirm the bug still triggers pre-fix
  )
done
```

Filtering the index programmatically:

```python
import json
bugs = json.load(open("index.json"))

reproducible  = [b for b in bugs if b["reproducible"]]
transformers  = [b for b in bugs if b["library"] == "transformers"]
by_library    = {}
for b in bugs:
    by_library.setdefault(b["library"], []).append(b["bug_id"])
```

**Recommendations**

- Run each bug in its own fresh virtualenv — dependency sets across bugs conflict by design
  (different library versions, CUDA builds, Python versions). `setup_env.sh` already isolates
  each bug in its own `.venv/`.
- Parallelize per-bug, but pin CPU/GPU resources; several bugs are memory- or GPU-hungry.
- For repair/agent evaluation, treat `run_repro.sh` exit + `reproduction.json` as the oracle:
  the bug is *fixed* when the reproduction no longer produces the reported signal.
- Start from the 533 `reproducible == true` bugs for clean pass/fail evaluation; the 107 others
  are useful for studying environment sensitivity and are labeled with why.

---

## 5. How the benchmark was built

Issues were mined from the target repositories' trackers and standardized into the per-bug
folder layout above. For each bug a minimal reproduction bundle (`repro.py`,
`requirements.txt`, `setup_env.sh`) was written, then the reproduction was executed in an
isolated virtualenv and its outcome recorded in `reproduction.json` and narrated in
`reproduction_trajectory.md`. `index.csv` / `index.json` summarize every bug (issue link,
commit, reproduction status) for setup and evaluation.

---

## Citation & license

If you use this benchmark, please cite the accompanying paper (see the Zenodo record for the
citation and DOI). Each bug's original report and source code remain under the license of its
upstream repository (`repository` / `clone_url` in `index.csv`); the packaging, reproduction
scripts, and metadata in this dataset are released under the license stated on the Zenodo
record.
