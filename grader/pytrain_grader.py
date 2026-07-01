"""Helpers every task grader (test_grade.py) uses to load the learner's code.

The runner (and selftest) set PYTRAIN_WS to the directory holding the
learner's files. Loading by explicit path — never by bare `import solution` —
guarantees the grader exercises the learner's file, not the reference
solution sitting next to the grader in the task directory.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest


def workspace() -> Path:
    """The directory holding the learner's files."""
    ws = os.environ.get("PYTRAIN_WS")
    if not ws:
        pytest.fail("PYTRAIN_WS is not set — run graders via `pytrain check` or selftest.py")
    return Path(ws)


def load_solution(filename: str = "solution.py", module_name: str = "solution"):
    """Import the learner's module from the workspace and return it.

    Fails the test (rather than erroring) with a clear message when the file
    is missing or raises at import time, so learners see a useful FAIL.
    """
    path = workspace() / filename
    if not path.exists():
        pytest.fail(f"{filename} not found in your workspace — did you run `pytrain start`?")
    # A unique module name per file avoids cross-test cache collisions when a
    # grader loads several learner files.
    unique = f"_pytrain_{module_name}_{abs(hash(str(path)))}"
    spec = importlib.util.spec_from_file_location(unique, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[unique] = mod
    # Let multi-file solutions import their sibling modules.
    ws = str(workspace())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:  # noqa: BLE001 — learner code can raise anything
        pytest.fail(f"importing your {filename} raised {type(e).__name__}: {e}")
    return mod


def get_attr(mod, name: str):
    """Fetch a required function/class from the learner's module, or FAIL clearly."""
    obj = getattr(mod, name, None)
    if obj is None:
        pytest.fail(f"your solution must define `{name}` (see the prompt)")
    return obj


def run_solution(*args: str, filename: str = "solution.py", input: str | None = None,
                 timeout: int = 30, check: bool = False) -> subprocess.CompletedProcess:
    """Run the learner's file as a script (for CLI/argparse tasks)."""
    path = workspace() / filename
    if not path.exists():
        pytest.fail(f"{filename} not found in your workspace")
    return subprocess.run(
        [sys.executable, str(path), *args],
        capture_output=True, text=True, input=input, timeout=timeout,
        check=check, cwd=str(workspace()),
    )


def time_limited(fn, *args, seconds: float = 5.0, **kwargs):
    """Run fn under a wall-clock budget; FAIL if it exceeds it.

    A blunt but portable complexity guard: graders pair a large-N call under
    time_limited() with small-N correctness asserts, so an O(n²) answer to an
    O(n log n) task times out rather than hanging the whole check.
    """
    import threading

    result, error = [], []

    def target():
        try:
            result.append(fn(*args, **kwargs))
        except Exception as e:  # noqa: BLE001
            error.append(e)

    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        pytest.fail(f"{getattr(fn, '__name__', 'function')} took longer than {seconds}s "
                    f"— check your algorithm's complexity")
    if error:
        raise error[0]
    return result[0]
