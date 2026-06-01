"""Summarise cProfile .prof outputs to generate an entry for the README."""

import pstats
from pathlib import Path

STRUCTURE_SET = 105
PACKAGES = ["ase", "pymatgen", "pycifrw", "pycifrw-fast", "parsnip", "gemmi"]
PROF_FILES = {pkg: f"{pkg}_{STRUCTURE_SET}.prof" for pkg in PACKAGES}

SKIP = {"~", "<frozen importlib", "benchmark.py"}


def top_call(stats):
    """First non-boilerplate function by cumulative time."""
    rows = sorted(stats.stats.items(), key=lambda kv: kv[1][3], reverse=True)
    for func, _ in rows:
        fname, _, ffunc = func
        if any(s in fname for s in SKIP):
            continue
        if ffunc.startswith("<built-in method") or ffunc == "<module>":
            continue
        return ffunc
    return "—"


for pkg in PACKAGES:
    path = Path(PROF_FILES[pkg])
    if not path.exists():
        continue
    stats = pstats.Stats(str(path))
    fn = top_call(stats)
    print(f"* `{PROF_FILES[pkg]}`: {stats.total_tt:.1f}s spent in `{fn}`")
