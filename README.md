# Benchmark DL Bugs

> **📢 MSR 2027 Mining Challenge dataset.** A reproducibility benchmark of real-world
> deep-learning bugs, packaged as self-contained, runnable reproductions.

<!-- TODO: fill in once the paper / dataset record exist -->
[![Paper](https://img.shields.io/badge/paper-arXiv-b31b1b.svg)](TODO)
[![Dataset](https://img.shields.io/badge/dataset-Zenodo-1682d4.svg)](TODO)
[![DOI](https://img.shields.io/badge/DOI-TODO-blue.svg)](TODO)

A reproducibility benchmark of **640 real-world deep-learning bugs** mined from the issue
trackers of **87 popular ML/DL repositories** across **63 organizations** — transformers, JAX,
vLLM, DeepSpeed, diffusers, PyTorch Lightning, TorchRL, PyG, detectron2, NumPyro, SDV, and more.

Every bug is packaged as a **self-contained, runnable reproduction**: a minimal script that
triggers the bug, the exact dependencies to install, a script that recreates the buggy codebase
at the offending commit, and a **reproduction trajectory** documenting how the bug was
reproduced and what was observed. Of the 640 bugs, **533 are verified reproducible** on the
reference machine; the remaining 107 ship with a documented, categorized reason they could not
be reproduced (hardware access, pinned builds, or upstream fixes).

| Bugs | Reproducible | Not reproducible | Repositories | Organizations | Package size |
|:----:|:------------:|:----------------:|:------------:|:-------------:|:------------:|
| **640** | **533** (83%) | **107** (17%) | **87** | **63** | ~48 MB |

<p align="center"><img src="assets/repro_status.png" alt="533 of 640 bugs reproduce (83%)" width="88%"></p>

> Codebases and Python environments are **regenerated on demand** (clone + checkout + venv), not
> shipped — which is why the whole package is ~48 MB rather than tens of gigabytes.

---

## Contents

1. [Key findings](#1-key-findings)
2. [What's in the package](#2-whats-in-the-package)
3. [Reproducing a single bug](#3-reproducing-a-single-bug)
4. [Running experiments across the benchmark](#4-running-experiments-across-the-benchmark)
5. [How the benchmark was built](#5-how-the-benchmark-was-built)
6. [Data notes & known limitations](#6-data-notes--known-limitations)
7. [Citation & license](#7-citation--license)

---

## 1. Key findings

**The dataset is broad and reproducible.** 533 of 640 bugs (83%) reproduce out of the box on a
single reference machine, spanning 87 repositories and 63 organizations. The Hugging Face stack
alone (transformers, diffusers, accelerate, peft, …) contributes 146 bugs; the Pyro/NumPyro
probabilistic-programming ecosystem 63; and the PyTorch, JAX, TensorFlow/Keras, vLLM, and
DeepSpeed families round out the rest.

<p align="center"><img src="assets/bugs_per_repo.png" alt="Bugs per repository, top 15, split by reproducibility" width="80%"></p>

**Reproducibility is gated by hardware, and the gate is concentrated in distributed / GPU-serving
libraries.** Reproduction rates are high and tight across most repositories (79–94%), but **vLLM
sits far below the pack at 44%** — and most of its non-reproducible bugs fail on GPU/accelerator
environment issues: broken or incompatible CUDA builds, missing or mismatched accelerators
(Hopper/H100), or multi-GPU topologies the single reference machine cannot provide. At the other
end, **NumPyro reproduces at 94%**: it is largely CPU-friendly probabilistic code with few
hardware dependencies. In other words, *what a library is for* predicts how reproducible its bugs
are on commodity hardware.

<p align="center"><img src="assets/repro_rate.png" alt="Reproduction rate by repository; vLLM lowest at 44%, NumPyro highest at 94%" width="78%"></p>

**When a bug doesn't reproduce, we say why.** Every one of the 107 non-reproducible cases carries
a `blocking_reason`. Grouping them:

<p align="center"><img src="assets/blocking_breakdown.png" alt="Breakdown of the 107 non-reproducible bugs" width="80%"></p>

| Category | Count | What it means |
|----------|:-----:|---------------|
| No longer reproduces on the pinned checkout | **61** (57%) | The standardized checkout no longer exhibits the reported behavior — fixed upstream, version drift, or nondeterministic/flaky. |
| Hardware / OS / build not available | **43** (40%) | Needs a GPU, multiple GPUs, ROCm/MPS, a specific OS, or a pinned build/dataset absent from the reference machine. |
| Not an executable bug | **3** (3%) | Documentation-only, a repo-tagging request, or otherwise non-code. |

The takeaway for tool builders: the 533 reproducible bugs give you a clean pass/fail oracle,
while the 107 non-reproducible cases are a *labeled* study set for environment sensitivity — most
are gated by hardware you can add, or by upstream fixes you can pin around.

> The 61 / 43 / 3 split is a coarse grouping of the free-text `blocking_reason` fields; the exact
> line between "fixed upstream" and "differs on this host" is judgment-dependent for a handful of
> cases. The precise per-bug reason is always in `index.csv` and each `reproduction.json`.

---

## 2. What's in the package

Each bug lives in its own numbered folder at the top level (`001/`, `002/`, …):

```
.
├── README.md                     # this file
├── assets/                       # figures used in this README
├── index.csv                     # ← START HERE: canonical bug_id → report/commit/status map
├── index.json                    # same index, for programmatic use
└── <bug_id>/                     # one folder per bug: 001, 002, … (zero-padded)
```

### `index.csv` — the map

One row per bug; the single source of truth for setup and evaluation:

| column | meaning |
|--------|---------|
| `bug_id`           | folder name (e.g. `001`) |
| `library`          | ML/DL library the bug belongs to (see [§6](#6-data-notes--known-limitations)) |
| `repository`       | GitHub `owner/repo` — the recommended grouping key |
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
where a plain clone was not sufficient — these are the only non-regenerable inputs and are kept
deliberately.

---

## 3. Reproducing a single bug

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

A reproducible bug fails (raises the reported error, produces the wrong result, etc.) exactly as
described in `bug_report.txt`. The expected signal, the exact steps, and the evidence are
documented in `reproduction_trajectory.md` and, in structured form, in `reproduction.json`
(`steps`, `evidence`, `reproducible`, `blocking_reason`, `reproduction_command`).

> **Python versions.** Bugs pin their own dependency sets and may need a specific interpreter
> (e.g. `python3.10`); `setup_env.sh` selects it. Install the required interpreter if it is not
> already on `PATH`.
>
> **GPU bugs.** Some bugs require a GPU (or multiple GPUs); their `blocking_reason` notes the
> hardware requirement. As [§1](#1-key-findings) shows, most of the 107 non-reproducible cases
> are hardware- or platform-gated, or fixed upstream.

---

## 4. Running experiments across the benchmark

The benchmark is designed for evaluating automated tools — bug reproducers, program-repair / APR
systems, agents, fault localizers. Typical loop:

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
import json, collections
bugs = json.load(open("index.json"))

reproducible = [b for b in bugs if b["reproducible"]]
transformers = [b for b in bugs if b["repository"] == "huggingface/transformers"]
by_repo = collections.defaultdict(list)
for b in bugs:
    by_repo[b["repository"]].append(b["bug_id"])   # group by repository, not library
```

**Recommendations**

- Run each bug in its own fresh virtualenv — dependency sets across bugs conflict by design
  (different library versions, CUDA builds, Python versions). `setup_env.sh` already isolates each
  bug in its own `.venv/`.
- Parallelize per-bug, but pin CPU/GPU resources; several bugs are memory- or GPU-hungry.
- For repair/agent evaluation, treat `run_repro.sh` exit + `reproduction.json` as the oracle: the
  bug is *fixed* when the reproduction no longer produces the reported signal.
- Start from the 533 `reproducible == true` bugs for clean pass/fail evaluation; the 107 others
  are useful for studying environment sensitivity and are labeled with why.
- Group by the `repository` column, not `library` — see [§6](#6-data-notes--known-limitations).

---

## 5. How the benchmark was built

Issues were mined from the target repositories' trackers and standardized into the per-bug folder
layout above. For each bug a minimal reproduction bundle (`repro.py`, `requirements.txt`,
`setup_env.sh`) was written, then the reproduction was executed in an isolated virtualenv and its
outcome recorded in `reproduction.json` and narrated in `reproduction_trajectory.md`.
`index.csv` / `index.json` summarize every bug (issue link, commit, reproduction status) for setup
and evaluation.

---

## 6. Data notes & known limitations

- **Group by `repository`, not `library`.** The `library` field is a free-text label carried over
  from mining and is not fully normalized: it contains casing duplicates (e.g. `SDV` and `sdv`)
  and, in at least one row, a full `owner/repo` string pasted into the column. Deduplicated, it
  resolves to ~100 distinct labels for the same **87 repositories**. For any grouping or
  per-project analysis, use the clean `repository` column.
- **Reproduction is single-machine.** "Reproducible" means *reproduced on the reference machine*.
  A bug marked not reproducible is not necessarily fixed — 40% of those cases simply need
  hardware (multi-GPU, ROCm/MPS, specific accelerators) or an OS/build the reference host didn't
  have. Check each `blocking_reason` before drawing conclusions.
- **Upstream state drifts.** Codebases are recreated from public repos at pinned commits; if an
  upstream repository is deleted or force-pushed, `setup_codebase.sh` for the affected bugs may
  need adjustment.

---

## 7. Citation & license

<!-- TODO: replace with the real citation/DOI once available -->
If you use this benchmark, please cite the accompanying paper:

```bibtex
@misc{benchmark_dl_bugs_2027,
  title  = {Benchmark DL Bugs: A Reproducibility Benchmark of Real-World Deep-Learning Bugs},
  author = {TODO},
  year   = {2027},
  note   = {MSR 2027 Mining Challenge dataset},
  doi    = {TODO}
}
```

Each bug's original report and source code remain under the license of its upstream repository
(`repository` / `clone_url` in `index.csv`); the packaging, reproduction scripts, and metadata in
this dataset are released under the license stated on the dataset record.
