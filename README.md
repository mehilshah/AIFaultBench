---
pretty_name: AIFaultBench
license: cc-by-4.0
language:
  - en
  - code
size_categories:
  - n<1K
task_categories:
  - other
tags:
  - software-engineering
  - bug-reproduction
  - fault-localization
  - automated-program-repair
  - debugging
  - benchmark
  - machine-learning
  - deep-learning
  - llm-infrastructure
  - agentic-ai
  - reinforcement-learning
  - msr
  - mining-software-repositories
configs:
  - config_name: default
    data_files:
      - split: train
        path: index.csv
---

# AIFaultBench: A Benchmark of Real-World Faults in AI Software Systems

[![Dataset on Zenodo](https://img.shields.io/badge/dataset-Zenodo-1682d4.svg)](https://doi.org/10.5281/zenodo.21422606)
[![Dataset on HF](https://img.shields.io/badge/dataset-%F0%9F%A4%97%20Hugging%20Face-yellow.svg)](https://huggingface.co/datasets/mehilshah/MSR-MiningChallenge-2027)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21422606.svg)](https://doi.org/10.5281/zenodo.21422606) 

AIFaultBench is a benchmark of **770 real-world AI software faults** collected from **105 open-source repositories** across **76 organizations**, spanning traditional machine learning, deep learning, large language model infrastructure, reinforcement learning, agentic AI systems, and AI tooling.

Each fault includes everything needed for reproduction:

* GitHub issue report
* Minimal reproduction script
* Dependency specification
* Codebase reconstruction script
* Environment setup script
* Reproduction logs
* Structured metadata
* Reproduction trajectory

**652 (85%) faults are verified reproducible**, while the remaining faults include documented reasons preventing reproduction.

| Bugs | Reproducible | Repositories | Organizations | Domains |
| ---: | -----------: | -----------: | ------------: | ------: |
|  770 |          652 |          105 |            76 |       6 |

---

## Dataset Overview

| Domain                 | Bugs | Reproducible |
| ---------------------- | ---: | -----------: |
| Deep Learning          |  307 |          83% |
| LLM Infrastructure     |  151 |          75% |
| Agentic AI             |  130 |          92% |
| Machine Learning       |  118 |          86% |
| Reinforcement Learning |   40 |          92% |
| AI Tooling             |   24 |         100% |

---

## Repository Structure

```
.
├── index.json
├── index.csv
├── consume_dataset.ipynb
├── bugs/
│   └── <bug_id>/
│       ├── bug_report.txt
│       ├── repro.py
│       ├── requirements.txt
│       ├── setup_codebase.sh
│       ├── setup_env.sh
│       ├── run_repro.sh
│       ├── reproduction.json
│       ├── reproduction_trajectory.md
│       └── logs/
```

The benchmark is indexed through both `index.json` and `index.csv`, while each bug is packaged independently inside `bugs/<bug_id>`.

---

## Quick Start

Reproducing a fault requires only Git, Python, and a POSIX-compatible shell.

```bash
cd bugs/<bug_id>
bash setup_codebase.sh
bash run_repro.sh
```

The scripts automatically

* reconstruct the buggy codebase,
* create an isolated Python environment,
* install dependencies,
* execute the reproduction script.

No Docker or API credentials are required.

---

## Loading the Dataset

```python
import json

bugs = json.load(open("index.json"))

reproducible = [b for b in bugs if b["reproducible"]]
agentic = [b for b in bugs if b["domain"] == "Agentic"]
```

The index is also exposed through the Hugging Face dataset viewer:

```python
from datasets import load_dataset

index = load_dataset("mehilshah/MSR-MiningChallenge-2027", split="train")
```

Note that `bug_id` is a zero-padded three-digit string (`001`, …, `774`) that names the
directory under `bugs/`. The CSV loader parses it as an integer, so pad it back before
building a path:

```python
path = f"bugs/{int(row['bug_id']):03d}"
```

Loading `index.json` directly preserves the identifier as a string.

For a complete walkthrough, see `consume_dataset.ipynb`.

---

## Package Contents

Each bug contains

* original GitHub issue
* minimal reproduction script
* dependency specification
* environment setup
* codebase reconstruction
* execution logs
* structured reproduction metadata
* reproduction trajectory

Together, these provide a fully executable reproduction package suitable for evaluating debugging, fault localization, automated repair, bug reproduction, and AI software engineering tools.

---

## Citation

```bibtex
@misc{AIFaultBench_2027,
  title={AIFaultBench: A Reproducible Benchmark of Real-World AI Software Faults},
  author={Shah, Mehil B and Rahman, Mohammad Masudur and Khomh, Foutse},
  year={2027},
  doi={10.5281/zenodo.21422606}
}
```

---

## License

The reproduction scripts, metadata, and benchmark packaging are released under
[CC BY 4.0](LICENSE).

Each original bug report and source repository remains under its respective upstream license.