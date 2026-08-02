#!/usr/bin/env python3
"""Regenerate the README figures in assets/ from index.csv, using LaTeX.

Each figure is emitted as a standalone TikZ / pgfplots document, compiled with
pdflatex and rasterised to PNG with pdftocairo. One design system, one data
source (index.csv) so the numbers can never drift from what ships.

Requires: a TeX distribution with pgfplots (pdflatex) and poppler (pdftocairo).
Run:  python3 scripts/make_figures.py
"""
from __future__ import annotations

import collections
import csv
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
DPI = 200

# --------------------------------------------------------------------------- #
# Ecosystem map: repository (last path component) -> family. Explicit and      #
# transparent; anything unmapped falls into "Other". Used only for the radar   #
# and the ecosystem rate-ranking; all counts still come from index.csv.        #
# --------------------------------------------------------------------------- #
FAMILY = {
    "Hugging Face": {"transformers", "diffusers", "accelerate", "peft",
                     "sentence-transformers", "safetensors", "adapters",
                     "evaluate", "datasets", "optimum", "open_clip"},
    "JAX": {"jax", "equinox", "jaxtyping", "flax"},
    "Probabilistic / stats": {"numpyro", "pyro", "SDV", "gpytorch", "bayesflow",
                              "optuna", "Ax", "POT"},
    "PyTorch vision / graph": {"pytorch-image-models", "detectron2",
                               "pytorch_geometric", "kornia", "vit-pytorch",
                               "denoising-diffusion-pytorch", "MONAI",
                               "anomalib", "Mask_RCNN", "torchio",
                               "imagen-pytorch", "vector-quantize-pytorch"},
    "Training / serving": {"vllm", "DeepSpeed", "pytorch-lightning", "torchtitan",
                           "lmdeploy", "NeMo", "unsloth", "axolotl", "torchtune",
                           "xformers", "triton", "Liger-Kernel", "whisperx"},
    "TensorFlow / Keras": {"models", "keras", "keras-io", "keras-cv", "keras-nlp",
                           "deepvariant"},
    "Reinforcement learning": {"rl", "stable-baselines3", "tianshou",
                               "PaLM-rlhf-pytorch"},
    "Agent frameworks": {"langgraph", "langchain", "smolagents", "pydantic-ai",
                         "camel", "crewAI", "autogen", "agno", "dspy",
                         "openai-agents-python", "SWE-agent", "semantic-kernel",
                         "langflow", "browser-use"},
    "RAG / memory / tracing": {"llama_index", "mem0", "phoenix", "python-sdk"},
}
FAMILY_ORDER = ["Hugging Face", "JAX", "Probabilistic / stats",
                "PyTorch vision / graph", "Training / serving",
                "TensorFlow / Keras", "Reinforcement learning",
                "Agent frameworks", "RAG / memory / tracing"]


def fam_of(repo: str) -> str:
    for name, repos in FAMILY.items():
        if repo in repos:
            return name
    return "Other"


# --------------------------------------------------------------------------- #
# LaTeX helpers                                                                #
# --------------------------------------------------------------------------- #
def tex_escape(s: str) -> str:
    return s.replace("\\", r"\textbackslash{}").replace("_", r"\_").replace(
        "&", r"\&").replace("%", r"\%").replace("#", r"\#")


PREAMBLE = r"""\documentclass[border=14pt,varwidth=%(vw)s]{standalone}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{pgfplots}
\usetikzlibrary{calc}
\pgfplotsset{compat=1.18}
\definecolor{good}{HTML}{0CA30C}
\definecolor{crit}{HTML}{D03B3B}
\definecolor{sone}{HTML}{2A78D6}
\definecolor{sonedark}{HTML}{1C5CAB}
\definecolor{sonesoft}{HTML}{9EC5F4}
\definecolor{ink}{HTML}{111111}
\definecolor{inktwo}{HTML}{52514E}
\definecolor{muted}{HTML}{7D7B76}
\definecolor{gridc}{HTML}{E1E0D9}
\definecolor{basec}{HTML}{C3C2B7}
\definecolor{surface}{HTML}{FCFCFB}
\definecolor{orange}{HTML}{EB6834}
\pagecolor{surface}
\pgfplotsset{
  barbase/.style={
    axis background/.style={fill=surface},
    axis line style={draw=none},
    tick style={draw=none},
    xmajorgrids, grid style={gridc, line width=0.5pt},
    xtick pos=bottom, ymin=-0.7,
    label style={font=\small\color{inktwo}},
    tick label style={font=\footnotesize\color{muted}},
    yticklabel style={color=ink, font=\small},
    clip=false,
  },
}
\newcommand{\FigTitle}[1]{{\noindent\bfseries\fontsize{15}{18}\selectfont\color{ink}#1\par}}
\newcommand{\FigSub}[1]{{\noindent\color{inktwo}\fontsize{10.5}{13.5}\selectfont#1\par\vspace{9pt}}}
\newcommand{\FigFoot}[1]{{\par\vspace{7pt}\noindent\color{muted}\fontsize{9}{11}\selectfont#1\par}}
\begin{document}
"""


def build(name: str, body: str, varwidth: str = "17cm") -> None:
    doc = (PREAMBLE % {"vw": varwidth}) + body + "\n\\end{document}\n"
    tmp = tempfile.mkdtemp(prefix="fig_")
    try:
        tex = os.path.join(tmp, name + ".tex")
        with open(tex, "w") as fh:
            fh.write(doc)
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex],
            cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        pdf = os.path.join(tmp, name + ".pdf")
        if r.returncode != 0 or not os.path.exists(pdf):
            log = os.path.join(tmp, name + ".log")
            err = open(log).read()[-2500:] if os.path.exists(log) else \
                r.stdout.decode("utf8", "replace")[-2500:]
            raise RuntimeError(f"pdflatex failed for {name}:\n{err}")
        out = os.path.join(ASSETS, name)
        subprocess.run(["pdftocairo", "-png", "-r", str(DPI), "-singlefile",
                        pdf, out], check=True)
        print("  wrote", name + ".png")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
# Data                                                                        #
# --------------------------------------------------------------------------- #
def load():
    with open(os.path.join(ROOT, "index.csv")) as fh:
        rows = list(csv.DictReader(fh))
    # index.csv serialises booleans Python-style ("True"/"False"); normalise so
    # the `== "true"` comparisons below cannot silently match nothing.
    for r in rows:
        r["reproducible"] = r["reproducible"].strip().lower()
        assert r["reproducible"] in ("true", "false"), r
    return rows


def per_repo(rows):
    d = collections.defaultdict(lambda: [0, 0])  # repo -> [total, repro]
    for r in rows:
        repo = r["repository"].split("/")[-1]
        d[repo][0] += 1
        d[repo][1] += r["reproducible"] == "true"
    return d


# --------------------------------------------------------------------------- #
# 1. Reproduction status — one headline stacked bar (hand-drawn TikZ)          #
# --------------------------------------------------------------------------- #
def fig_status(rows):
    total = len(rows)
    repro = sum(r["reproducible"] == "true" for r in rows)
    notr = total - repro
    W = 15.5  # cm
    wr = repro / total * W
    wn = notr / total * W
    gap = 0.06
    body = r"""
\FigTitle{Reproduction status of the benchmark}
\FigSub{%(repro)d of %(total)d AI/ML bugs reproduce on the reference machine (%(pct)d\%%).}
\begin{tikzpicture}[x=1cm,y=1cm]
  \fill[good] (0,0) rectangle (%(wr).3f,1.5);
  \fill[crit] (%(xn).3f,0) rectangle (%(W).3f,1.5);
  \node[white] at (%(cr).3f,0.92) {\bfseries\large Reproducible};
  \node[white] at (%(cr).3f,0.50) {\normalsize %(repro)d \;\textbullet\; %(pct)d\%%};
  \node[white] at (%(cn).3f,0.92) {\bfseries Not repro.};
  \node[white] at (%(cn).3f,0.50) {\footnotesize %(notr)d \;\textbullet\; %(pctn)d\%%};
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; n = %(total)d bugs}
""" % dict(total=total, repro=repro, notr=notr,
           pct=round(repro / total * 100), pctn=round(notr / total * 100),
           W=W, wr=wr, xn=wr + gap, cr=wr / 2, cn=wr + gap + wn / 2)
    build("repro_status", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 2. Bugs per repository (top 15), stacked repro / not-repro                   #
# --------------------------------------------------------------------------- #
def fig_bugs_per_repo(rows):
    d = per_repo(rows)
    items = sorted(d.items(), key=lambda x: x[1][0], reverse=True)[:15]
    items.reverse()  # largest at top (barh)
    coords_r, coords_n, ylabels, totlabels = [], [], [], []
    for i, (repo, (tot, rp)) in enumerate(items):
        coords_r.append(f"({rp},{i})")
        coords_n.append(f"({tot - rp},{i})")
        ylabels.append(tex_escape(repo))
        totlabels.append(rf"\node[anchor=west,color=ink,font=\small\bfseries] "
                         rf"at (axis cs:{tot},{i}) {{\;{tot}}};")
    n = len(items)
    body = r"""
\FigTitle{Bugs per repository}
\FigSub{Top 15 repositories by bug count, split by whether each bug reproduces.}
\begin{tikzpicture}
\begin{axis}[barbase, xbar stacked, width=15.5cm, height=10.5cm,
  bar width=13pt, xmin=0, xmax=%(xmax)d, ymax=%(ymax).1f,
  ytick={0,...,%(last)d}, yticklabels={%(ylabels)s},
  legend style={draw=none, fill=surface, font=\small, at={(0.98,0.04)},
    anchor=south east, legend columns=1},
  area legend,
  ]
  \addplot[fill=good,draw=none] coordinates {%(cr)s};
  \addplot[fill=crit,draw=none] coordinates {%(cn)s};
  \legend{Reproducible, Not reproducible}
%(tot)s
\end{axis}
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; number at bar end is the repo's total bug count}
""" % dict(xmax=max(t for _, (t, _) in items) + 4, ymax=n - 0.3, last=n - 1,
           ylabels=",".join(ylabels), cr=" ".join(coords_r),
           cn=" ".join(coords_n), tot="\n".join(totlabels))
    build("bugs_per_repo", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 3. Reproduction rate by repository (>= 15 bugs), single hue + mean line      #
# --------------------------------------------------------------------------- #
def fig_rate(rows):
    d = per_repo(rows)
    avg = sum(r["reproducible"] == "true" for r in rows) / len(rows) * 100
    items = [(repo, rp / tot * 100) for repo, (tot, rp) in d.items() if tot >= 15]
    items.sort(key=lambda x: x[1])  # worst bottom, best top
    blue, red = [], []
    ylabels, labels = [], []
    for i, (repo, rate) in enumerate(items):
        (red if repo == "vllm" else blue).append(f"({rate:.2f},{i})")
        ylabels.append(tex_escape(repo))
        col = "crit" if repo == "vllm" else "ink"
        labels.append(rf"\node[anchor=west,color={col},font=\small\bfseries] "
                      rf"at (axis cs:{rate:.2f},{i}) {{\;{rate:.0f}\%}};")
    n = len(items)
    body = r"""
\FigTitle{Reproduction rate by repository}
\FigSub{Repositories with $\geq$ 15 bugs. GPU-serving / distributed libraries (vLLM) reproduce least; CPU-friendly ones (NumPyro) most.}
\begin{tikzpicture}
\begin{axis}[barbase, xbar, width=15cm, height=10.5cm, bar width=12pt,
  xmin=0, xmax=112, ymax=%(ymax).1f, xtick={0,20,40,60,80,100},
  xticklabel={\pgfmathprintnumber{\tick}\%%},
  ytick={0,...,%(last)d}, yticklabels={%(ylabels)s}, y=0.62cm,
  ]
  \addplot[fill=sone,draw=none] coordinates {%(blue)s};
  \addplot[fill=crit,draw=none] coordinates {%(red)s};
  \draw[muted, dashed, line width=1pt] (axis cs:%(avg).2f,-0.7) -- (axis cs:%(avg).2f,%(ymax).1f);
  \node[anchor=south west, color=muted, font=\footnotesize] at (axis cs:%(avg).2f,%(ymax).1f) {\;dataset avg %(avgr)d\%%};
%(labels)s
\end{axis}
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; bars show the share of that repo's bugs that reproduce}
""" % dict(ymax=n - 0.3, last=n - 1, ylabels=",".join(ylabels),
           blue=" ".join(blue), red=" ".join(red) or "(-1,-1)",
           avg=avg, avgr=round(avg), labels="\n".join(labels))
    build("repro_rate", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 4. Why the non-reproducible bugs don't reproduce (sequential blue)          #
# --------------------------------------------------------------------------- #
def fig_blocking(rows):
    notr = sum(r["reproducible"] != "true" for r in rows)
    # Manual grouping of the free-text `blocking_reason` field. The first three
    # counts are the original hand grouping over the 107 pre-agentic blocked
    # cases (61/43/3); the agentic split added 8 / 2 / 1 respectively.
    cats = [
        ("No longer reproduces on the pinned\\\\checkout (fixed / drift / flaky)", 69, "sonedark"),
        ("Hardware / OS / build not\\\\available on the reference machine", 45, "sone"),
        ("Not an executable bug\\\\(docs, meta, non-code)", 4, "sonesoft"),
    ]
    assert sum(c[1] for c in cats) == notr, (
        f"manual blocking grouping sums to {sum(c[1] for c in cats)}, "
        f"but index.csv has {notr} non-reproducible bugs")
    cats = cats[::-1]
    plots, labels, ylabels = [], [], []
    for i, (lab, v, col) in enumerate(cats):
        plots.append(rf"\addplot[fill={col},draw=none,xbar] coordinates {{({v},{i})}};")
        labels.append(rf"\node[anchor=west,color=ink,font=\small\bfseries] "
                      rf"at (axis cs:{v},{i}) {{\;{v} \;\textbullet\; {round(v/notr*100)}\%}};")
        ylabels.append(r"{\footnotesize\begin{tabular}{@{}r@{}}" +
                       lab.replace("\\\\", r"\\") + r"\end{tabular}}")
    body = r"""
\FigTitle{Why %(notr)d bugs don't reproduce here}
\FigSub{The reference machine is CPU-first; most blocked cases are upstream fixes or unavailable hardware.}
\begin{tikzpicture}
\begin{axis}[barbase, width=15cm, height=5.2cm, bar width=15pt,
  xmin=0, xmax=74, ymax=2.4, xtick={0,20,40,60},
  ytick={0,1,2}, yticklabels={%(ylabels)s}, y=1.15cm,
  ]
%(plots)s
%(labels)s
\end{axis}
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; n = %(notr)d non-reproducible bugs}
""" % dict(notr=notr, ylabels=",".join(ylabels), plots="\n".join(plots),
           labels="\n".join(labels))
    build("blocking_breakdown", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 5. Reliability ranking by ecosystem — lollipop dot plot with mean line       #
# --------------------------------------------------------------------------- #
def fig_rate_ranking(rows):
    d = per_repo(rows)
    fam = collections.defaultdict(lambda: [0, 0])
    for repo, (tot, rp) in d.items():
        f = fam_of(repo)
        fam[f][0] += tot
        fam[f][1] += rp
    avg = sum(r["reproducible"] == "true" for r in rows) / len(rows) * 100
    items = [(f, fam[f][1] / fam[f][0] * 100, fam[f][0]) for f in FAMILY_ORDER]
    items.sort(key=lambda x: x[1])
    stems, dots, labels, ylabels = [], [], [], []
    xmin = 55
    for i, (f, rate, tot) in enumerate(items):
        col = "good" if rate >= avg else "crit"
        stems.append(rf"\draw[basec,line width=1.4pt] (axis cs:{xmin},{i}) -- (axis cs:{rate:.2f},{i});")
        dots.append(rf"\addplot[only marks,mark=*,mark size=3.6pt,color={col}] coordinates {{({rate:.2f},{i})}};")
        labels.append(rf"\node[anchor=west,color=ink,font=\small\bfseries] at (axis cs:{rate:.2f},{i}) {{\;\;{rate:.0f}\%}};")
        ylabels.append(tex_escape(f))
    n = len(items)
    body = r"""
\FigTitle{Reliability ranking by ecosystem}
\FigSub{Reproducibility rate per ecosystem family (repos grouped by project). The dashed line is the %(avgr)d\%% dataset mean; \textcolor{crit}{red} dots under-perform it.}
\begin{tikzpicture}
\begin{axis}[barbase, width=15cm, height=7.2cm, xmin=%(xmin)d, xmax=104,
  ymax=%(ymax).1f, xtick={60,70,80,90,100},
  xticklabel={\pgfmathprintnumber{\tick}\%%},
  ytick={0,...,%(last)d}, yticklabels={%(ylabels)s}, y=0.8cm,
  ]
%(stems)s
  \draw[muted, dashed, line width=1pt] (axis cs:%(avg).2f,-0.7) -- (axis cs:%(avg).2f,%(ymax).1f);
  \node[anchor=south, color=muted, font=\footnotesize] at (axis cs:%(avg).2f,%(ymax).1f) {mean %(avgr)d\%%};
%(dots)s
%(labels)s
\end{axis}
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; ecosystem = explicit repo$\rightarrow$family grouping (see scripts/make\_figures.py)}
""" % dict(avgr=round(avg), avg=avg, xmin=xmin, ymax=n - 0.3, last=n - 1,
           ylabels=",".join(ylabels), stems="\n".join(stems),
           dots="\n".join(dots), labels="\n".join(labels))
    build("rate_ranking", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 6. Does volume hurt reproducibility? — bubble scatter                        #
# --------------------------------------------------------------------------- #
def fig_volume_vs_rate(rows):
    d = per_repo(rows)
    avg = sum(r["reproducible"] == "true" for r in rows) / len(rows) * 100
    pts = [(repo, tot, rp / tot * 100) for repo, (tot, rp) in d.items()]
    bubbles = []
    for repo, tot, rate in pts:
        col = "crit" if repo == "vllm" else "sone"
        op = "0.9" if repo == "vllm" else "0.5"
        bubbles.append(
            rf"\addplot[only marks,mark=*,mark options={{fill={col},fill opacity={op},"
            rf"draw={col},draw opacity=0.9}},mark size={{{0.9 + tot**0.5*0.7:.2f}pt}}] "
            rf"coordinates {{({tot},{rate:.2f})}};")
    # label a few notable repos (avoid overlapping identical coordinates)
    ann = []
    for repo, tot, rate in pts:
        if repo == "vllm":
            ann.append(rf"\node[color=crit,font=\footnotesize\bfseries,anchor=west,xshift=0.32cm] "
                       rf"at (axis cs:{tot},{rate:.2f}) {{vLLM \textbullet\ 44\%}};")
        elif repo == "numpyro":
            ann.append(rf"\node[color=inktwo,font=\footnotesize,anchor=north,yshift=-0.42cm] "
                       rf"at (axis cs:{tot},{rate:.2f}) {{numpyro}};")
    body = r"""
\FigTitle{Does artifact volume hurt reproducibility?}
\FigSub{Each bubble is a repository: x = bugs contributed, y = reproducibility rate, size $\propto$ bug count. Mostly flat --- big repos reproduce fine. vLLM is the clear outlier.}
\begin{tikzpicture}
\begin{axis}[
  axis background/.style={fill=surface},
  width=15cm, height=9cm,
  axis line style={basec}, tick style={draw=none},
  xmajorgrids, ymajorgrids, grid style={gridc, line width=0.5pt},
  xmin=0, xmax=42, ymin=38, ymax=102,
  xlabel={Bugs contributed}, ylabel={Reproducibility rate},
  ytick={40,60,80,100}, yticklabel={\pgfmathprintnumber{\tick}\%%},
  label style={font=\small\color{inktwo}},
  tick label style={font=\footnotesize\color{muted}}, clip=true,
  ]
  \draw[muted, dashed, line width=1pt] (axis cs:0,%(avg).2f) -- (axis cs:42,%(avg).2f);
  \node[anchor=south, color=muted, font=\footnotesize] at (axis cs:17.5,%(avg).2f) {mean %(avgr)d\%%};
%(bub)s
%(ann)s
\end{axis}
\end{tikzpicture}
\FigFoot{Source: index.csv \;\textbullet\; one bubble per repository (%(nrepo)d total)}
""" % dict(avg=avg, avgr=round(avg), bub="\n".join(bubbles),
           ann="\n".join(ann), nrepo=len(pts))
    build("volume_vs_rate", body, varwidth="17cm")


# --------------------------------------------------------------------------- #
# 7. Ecosystem reproducibility radar (hand-drawn TikZ)                          #
# --------------------------------------------------------------------------- #
def fig_radar(rows):
    import math
    d = per_repo(rows)
    fam = collections.defaultdict(lambda: [0, 0])
    for repo, (tot, rp) in d.items():
        f = fam_of(repo)
        fam[f][0] += tot
        fam[f][1] += rp
    avg = sum(r["reproducible"] == "true" for r in rows) / len(rows) * 100
    vals = [(f, fam[f][1] / fam[f][0] * 100, fam[f][0]) for f in FAMILY_ORDER]
    N = len(vals)
    Rmax = 4.2                  # cm at 100%
    floor = 40.0                # inner value of the radar (0% would waste space)
    def rad(v):
        return (v - floor) / (100 - floor) * Rmax
    def ang(i):
        return 90 - i * 360.0 / N

    parts = [r"\begin{tikzpicture}[x=1cm,y=1cm]"]
    # rings + ring labels
    for gv in (40, 60, 80, 100):
        r = rad(gv)
        parts.append(rf"\draw[gridc,line width=0.6pt] (0,0) circle ({r:.3f});")
        parts.append(rf"\node[muted,font=\tiny,fill=surface,inner sep=0.5pt] at (0,{r:.3f}) {{{gv}\%}};")
    # mean ring (dashed)
    parts.append(rf"\draw[muted,dashed,line width=0.9pt] (0,0) circle ({rad(avg):.3f});")
    # spokes + axis labels
    label_r = Rmax + 0.35
    for i, (f, v, tot) in enumerate(vals):
        a = ang(i)
        x = math.cos(math.radians(a)) * Rmax
        y = math.sin(math.radians(a)) * Rmax
        parts.append(rf"\draw[basec,line width=0.6pt] (0,0) -- ({x:.3f},{y:.3f});")
        lx = math.cos(math.radians(a)) * label_r
        ly = math.sin(math.radians(a)) * label_r
        anchor = "west" if -90 < a < 90 else ("east" if abs(a) > 90 else "center")
        if abs(abs(a) - 90) < 1:
            anchor = "south" if a > 0 else "north"
        # wrap long labels
        fl = tex_escape(f).replace(" / ", r" /\\ ")
        parts.append(rf"\node[anchor={anchor},align=center,color=ink,font=\footnotesize] "
                     rf"at ({lx:.3f},{ly:.3f}) {{\begin{{tabular}}{{@{{}}c@{{}}}}{fl}\\[-1pt]"
                     rf"{{\color{{inktwo}}\scriptsize {v:.0f}\%}}\end{{tabular}}}};")
    # value polygon
    poly = []
    for i, (f, v, tot) in enumerate(vals):
        a = ang(i)
        r = rad(v)
        poly.append(f"({math.cos(math.radians(a))*r:.3f},{math.sin(math.radians(a))*r:.3f})")
    parts.append(r"\fill[sone,opacity=0.16] " + " -- ".join(poly) + " -- cycle;")
    parts.append(r"\draw[sone,line width=1.6pt] " + " -- ".join(poly) + " -- cycle;")
    for p in poly:
        parts.append(rf"\fill[sone] {p} circle (2.4pt);")
        parts.append(rf"\draw[surface,line width=0.8pt] {p} circle (2.4pt);")
    parts.append(r"\end{tikzpicture}")
    body = r"""
\FigTitle{Reproducibility across ecosystems}
\FigSub{Reproducibility rate for each ecosystem family. The dashed ring is the %(avgr)d\%% dataset mean; families outside it beat the average.}
\begin{center}
%(pic)s
\end{center}
\FigFoot{Source: index.csv \;\textbullet\; radial axis 40--100\%% \;\textbullet\; ecosystem = explicit repo$\rightarrow$family grouping}
""" % dict(avgr=round(avg), pic="\n".join(parts))
    build("ecosystem_radar", body, varwidth="13cm")


def main():
    rows = load()
    print("Generating LaTeX figures ->", ASSETS)
    fig_status(rows)
    fig_bugs_per_repo(rows)
    fig_rate(rows)
    fig_blocking(rows)
    fig_rate_ranking(rows)
    fig_volume_vs_rate(rows)
    fig_radar(rows)
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
