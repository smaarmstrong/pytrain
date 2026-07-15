# Authoring tasks

A task is a directory `tasks/<domain>/<nn-name>/` (two-digit `nn` orders the
domain from fundamentals to advanced). It contains:

| file | required | purpose |
|---|---|---|
| `meta.json` | yes | metadata (schema below) |
| `prompt.md` | yes | the spec the learner reads |
| `starter.py` | no | scaffold copied to the workspace as `solution.py` |
| `starter/` | no | multi-file scaffold (copied verbatim; use instead of `starter.py`) |
| `test_grade.py` | yes | pytest grader, run against the learner's workspace |
| `solution.py` | yes* | reference solution (`solution/` dir for multi-file tasks) |
| `learn.md` | no | interactive lesson shown by `pytrain learn` (see below) |

## meta.json

```json
{
  "title": "K smallest, lazily",
  "domain": "dsa",
  "objective": "heaps: heapq k-smallest / merge k sorted / priority queue with tie-breaks",
  "difficulty": 2,
  "est_min": 15,
  "deps": [],
  "tags": [],
  "python": "3.12",
  "timeout": 120
}
```

- `objective` — copy the matching line from `docs/objectives.md` verbatim.
- `difficulty` — 1..5 (drives XP: 10/15/25/40/60).
- `deps` — third-party packages the *grader venv* needs (e.g. `["fastapi", "httpx"]`).
  Empty for stdlib-only tasks. pytest is always present. Pin nothing unless a
  behaviour genuinely requires it.
- `tags` — `["advanced"]` for bonus material.
- `python` — optional minimum interpreter (e.g. PEP 695 tasks: `"3.12"`).
- `timeout` — optional whole-grader wall-clock cap in seconds (default 120).

## The grader contract

`test_grade.py` is executed by pytest inside the task's venv with:

- `PYTRAIN_WS` = the learner's workspace directory
- `PYTHONPATH` = the repo's `grader/` dir, so it can `import pytrain_grader`
- cwd = the workspace

Load learner code **only** via `pytrain_grader`:

```python
from pytrain_grader import load_solution, get_attr

def test_reverses():
    mod = load_solution()                 # learner's solution.py, by path
    reverse = get_attr(mod, "reverse")    # clear FAIL if missing
    assert reverse([1, 2, 3]) == [3, 2, 1]
```

Also available: `run_solution(*args)` (run the learner file as a script, for
CLI tasks) and `time_limited(fn, big_input, seconds=5)` (portable complexity
budget — pair a large-N call with small-N correctness asserts).

Never `import solution` directly — pytest would resolve it to the *reference*
solution sitting next to the grader.

## `learn.md` (optional lesson)

The interactive lesson `pytrain learn` walks a learner through *before* they
attempt the task — for someone meeting the material for the first time, not just
being tested on it. Optional: with no `learn.md`, `learn` falls back to showing
the prompt and offering to set up the workspace.

`learn` reads it as a **tutor script** — plain readable prose plus two markers:

- A line that is exactly `---` is a **pause**: the tutor prints everything above
  it, then waits ("Enter to continue") before going on. Use it to break the
  lecture into digestible beats.
- A fenced ```` ```run ```` block is a **snippet to try**. The tutor shows it and
  runs it live as a **single Python script** (this interpreter, in a throwaway
  temp dir) so the learner sees real output. Captured verbatim, so multi-line
  functions, classes and loops survive. Make snippets `print(...)` what they
  demonstrate. Keep a block to one logical step; use several blocks for several.

Everything else prints as-is, so write plain text, not heavy Markdown. House
style is five sections, interleaved with `---` pauses and ```` ```run ```` steps:

```
THE IDEA        what the thing is and the mental model for it
WHY IT MATTERS  why a working programmer cares
HOW TO DO IT    the actual constructs (as ```run steps), explained as you go
CHECK IT WORKED how the pieces map onto the task's functions
GOTCHAS         the classic traps
```

Because the snippets run for real, a lesson may end with the concept fully
demonstrated — `learn` then offers a clean solo attempt (`start` re-creates the
workspace from the starter). A good lesson teaches the *skill* so the solution
becomes obvious; it must never be just a reworded `solution.py`.

**Pedagogy standard.** Assume the learner knows almost nothing. Never make them
run something they couldn't reconstruct from understanding — no unexplained
one-liners, regex, or clever tricks dropped as incantations. If a step uses a
non-obvious construct, teach it inline in plain English first, or use the
simplest approach. Order material so foundations come before anything that leans
on them. See `tasks/core/01-fstring-formatting` … `05-exception-hierarchy` for
worked examples.

## Quality bars

1. **Behaviour, not style.** Assert what the code does — results, side
   effects, raised exceptions — never how it's written. Any correct
   implementation must pass, including ones very different from the reference.
2. **Selftest-proof.** The grader must FAIL on the starter/empty stub and PASS
   on the reference solution. `./selftest.py <domain>/<nn-name>` before
   committing — it checks exactly that, in throwaway workspaces.
3. **Deterministic.** Seed all randomness (grader *and* generated fixtures).
   No network, no live servers (use test clients / mock transports), no
   reliance on wall-clock dates, locale, or dict-ordering accidents beyond the
   language guarantee.
4. **Edge cases.** Empty inputs, single elements, duplicates, boundaries — a
   plausible-but-buggy solution should fail, not squeak by.
5. **Helpful failure.** Prefer several focused tests with clear names over one
   mega-test; the learner sees pytest's output.
6. **Cross-platform.** Pure Python; `pathlib` over string paths; no shelling
   out to Unix-only tools.
7. **Deps minimal and honest.** Declare exactly what the grader imports.
   Framework tasks grade through test clients (`fastapi.testclient`,
   `flask.test_client`, Django's `Client`) — never bind ports.
8. **prompt.md is a spec**: state the file to create (usually `solution.py`),
   the exact function/class names and signatures, behaviour incl. edge cases
   and errors, and 1-2 usage examples. Don't reveal the algorithm unless
   teaching it is the point.
