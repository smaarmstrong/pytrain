# pytrain

A console trainer for the whole Python language and ecosystem — same DNA as
[smaarmstrong/redhat](https://github.com/smaarmstrong/redhat), but for code:
every task is a real, well-specified piece of code to write, and the grader is
a **pytest suite run against your file** in an isolated venv. Deterministic,
behaviour-only grading — any correct implementation passes.

```
git clone https://github.com/smaarmstrong/pytrain
cd pytrain
make learn                         # teach the next task, then set up its workspace
$EDITOR workspace/core/01-fstring-formatting/solution.py
make check                         # grade the task you're on; then `make learn` again
```

New to the material? `learn` / `train` decide what's next for you — no need to
pick task ids. Prefer the raw CLI? Every `make` target forwards to `./bin/pytrain`:

```
./bin/pytrain train                # auto-pick: a due review, else the next new task
./bin/pytrain start dsa/06-heapq-ksmallest
$EDITOR workspace/dsa/06-heapq-ksmallest/solution.py
./bin/pytrain check dsa/06-heapq-ksmallest
```

Needs only Python ≥ 3.11. [`uv`](https://docs.astral.sh/uv/) is used for fast
venv provisioning when present, otherwise `venv` + `pip`. Bare `make` prints the
available targets and changes nothing.

## Commands

| command | what it does |
|---|---|
| `pytrain learn [id]` | tutor a task (its `learn.md`, then a solo attempt); no id ⇒ the next new task |
| `pytrain train` | auto-pick what to do next: a due spaced-repetition review, else the next new task in teaching order |
| `pytrain list [domain]` | tasks grouped by domain, with your status |
| `pytrain start <id>` | create `workspace/<id>/` from the starter and show the spec |
| `pytrain check [id]` | run the task's pytest grader against your solution |
| `pytrain solution [id]` | reveal a reference solution |
| `pytrain reset [id]` | restore the starter (your work is backed up to `*.bak`) |
| `pytrain status` | XP, daily streak, per-domain progress bars |

`<id>` is `domain/nn-name`, or just the unique trailing name. For
`check`/`solution`/`reset` you can omit it to act on the task `train`/`start`
last handed you. Progress lives in `~/.local/state/pytrain/progress.json`; XP
scales with difficulty and the streak counts consecutive days with at least one
pass.

## How `train` picks

`train` runs a small spaced-repetition scheduler. New material is served in a
**fundamentals-first teaching order** (core → stdlib → dsa → oop → typing →
testing → concurrency → packaging → web → data → projects; within a domain the
`nn-` prefix runs easy→hard). Each pass schedules the task for review on a
widening ladder (1, 3, 7, 16, 35, 75 days, then doubling); a later failure is a
lapse and resets it to relearn soon. Due reviews take priority — but never more
than two in a row while new material is still waiting, so you keep advancing.

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
