# pytrain

A console trainer for the whole Python language and ecosystem — same DNA as
[smaarmstrong/redhat](https://github.com/smaarmstrong/redhat), but for code:
every task is a real, well-specified piece of code to write, and the grader is
a **pytest suite run against your file** in an isolated venv. Deterministic,
behaviour-only grading — any correct implementation passes.

```
git clone https://github.com/smaarmstrong/pytrain
cd pytrain
./bin/pytrain list                 # all tasks, grouped by domain
./bin/pytrain start dsa/06-heapq-ksmallest
$EDITOR workspace/dsa/06-heapq-ksmallest/solution.py
./bin/pytrain check dsa/06-heapq-ksmallest
```

Needs only Python ≥ 3.11. [`uv`](https://docs.astral.sh/uv/) is used for fast
venv provisioning when present, otherwise `venv` + `pip`.

## Commands

| command | what it does |
|---|---|
| `pytrain list [domain]` | tasks grouped by domain, with your status |
| `pytrain start <id>` | create `workspace/<id>/` from the starter and show the spec |
| `pytrain check <id>` | run the task's pytest grader against your solution |
| `pytrain solution <id>` | reveal a reference solution |
| `pytrain reset <id>` | restore the starter (your work is backed up to `*.bak`) |
| `pytrain status` | XP, daily streak, per-domain progress bars |

`<id>` is `domain/nn-name`, or just the unique trailing name. Progress lives
in `~/.local/state/pytrain/progress.json`; XP scales with difficulty and the
streak counts consecutive days with at least one pass.

## Domains

`core` language fundamentals · `dsa` data structures & algorithms · `stdlib`
standard library · `oop` OOP & design patterns · `typing` static typing (mypy)
· `concurrency` threading/multiprocessing/asyncio · `testing` pytest & quality
tooling · `packaging` pyproject/build/uv · `web` Flask/FastAPI/Django ·
`data` numpy/pandas/polars/matplotlib/sklearn/SQLAlchemy · `projects`
multi-file composites.

The full coverage checklist is [docs/objectives.md](docs/objectives.md).

## How grading works

Each task directory holds `meta.json`, `prompt.md`, an optional starter,
`test_grade.py` (the grader) and a reference `solution.py`. `check` provisions
a **cached venv per dependency set** (so the first pandas task installs once,
every later pandas task is instant), points the grader at your workspace via
`PYTRAIN_WS`, and runs pytest. Tasks that need packages you can't install
(offline?) are reported as SKIP with a note, never as failures.

Graders assert behaviour and edge cases, never style. Randomness is seeded.
DSA tasks with complexity requirements enforce them with wall-clock budgets on
large inputs.

## Selftest

`./selftest.py` proves every grader is neither too lax nor too strict: in a
throwaway workspace it must **FAIL on the starter stub** and **PASS on the
reference solution**. Run it after authoring or changing any task.

## Authoring tasks

See [docs/authoring.md](docs/authoring.md) for the task format and quality
bars.
