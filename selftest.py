#!/usr/bin/env python3
"""
selftest.py — prove every grader is neither too lax nor too strict.

For each task, in a throwaway workspace:
    grader vs starter/empty stub   -> expect FAIL   (catches pre-satisfied graders)
    grader vs reference solution   -> expect PASS   (catches wrong/over-strict graders)

Venvs are the same cached-per-dep-set ones `pytrain check` uses, provisioned
serially up front so parallel grading never races an install.

Usage:
    ./selftest.py                       # every task
    ./selftest.py dsa/03-heapq web      # specific tasks and/or whole domains
    ./selftest.py --offline             # skip tasks that need third-party deps
    ./selftest.py -j 8                  # grading parallelism (default 4)
"""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parent

# bin/pytrain has no .py extension; load it as a module to reuse its logic.
_spec = importlib.util.spec_from_file_location(
    "pytrain_runner", REPO / "bin" / "pytrain",
    loader=importlib.machinery.SourceFileLoader("pytrain_runner", str(REPO / "bin" / "pytrain")),
)
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)

GRN = runner.GRN; RED = runner.RED; YEL = runner.YEL; DIM = runner.DIM


def make_ws(task_dir: Path, kind: str) -> Path:
    """Build a throwaway workspace: 'stub' from the starter, 'solution' from the reference."""
    ws = Path(tempfile.mkdtemp(prefix=f"pytrain-selftest-{kind}-"))
    if kind == "solution":
        sol_dir = task_dir / "solution"
        if sol_dir.is_dir():
            shutil.copytree(sol_dir, ws, dirs_exist_ok=True)
        else:
            shutil.copy(task_dir / "solution.py", ws / "solution.py")
    else:
        starter_dir = task_dir / "starter"
        if starter_dir.is_dir():
            shutil.copytree(starter_dir, ws, dirs_exist_ok=True)
        elif (task_dir / "starter.py").exists():
            shutil.copy(task_dir / "starter.py", ws / "solution.py")
        else:
            (ws / "solution.py").write_text('"""stub"""\n')
    return ws


def run_grader(exe: str, task_dir: Path, ws: Path, timeout: int) -> tuple[bool, str]:
    env = os.environ.copy()
    env["PYTRAIN_WS"] = str(ws)
    env["PYTHONPATH"] = str(REPO / "grader")
    env.pop("PYTEST_ADDOPTS", None)
    try:
        proc = subprocess.run(
            [exe, "-m", "pytest", str(task_dir / "test_grade.py"), "-q", "--no-header",
             "-p", "no:cacheprovider", "--rootdir", str(ws), "--tb=line"],
            capture_output=True, text=True, env=env, cwd=str(ws),
            stdin=subprocess.DEVNULL, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, "grader timed out"
    return proc.returncode == 0, proc.stdout + proc.stderr


def selftest_one(tid: str, meta: dict) -> tuple[str, str, str]:
    """Returns (tid, verdict, detail): verdict in {ok, fail, skip}."""
    if not runner.task_python_ok(meta):
        return tid, "skip", f"needs Python >= {meta['python']}"
    exe, note = runner.venv_for(meta.get("deps", []))
    if note:
        return tid, "skip", note.splitlines()[0]
    timeout = meta.get("timeout", 120)
    problems = []

    ws = make_ws(meta["_dir"], "stub")
    try:
        passed, _ = run_grader(exe, meta["_dir"], ws, timeout)
        if passed:
            problems.append("grader PASSES on the empty/starter stub (too lax)")
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    ws = make_ws(meta["_dir"], "solution")
    try:
        passed, out = run_grader(exe, meta["_dir"], ws, timeout)
        if not passed:
            tail = "\n".join(out.strip().splitlines()[-6:])
            problems.append("grader FAILS on the reference solution (too strict/wrong):\n" +
                            "\n".join("      " + l for l in tail.splitlines()))
    finally:
        shutil.rmtree(ws, ignore_errors=True)

    if problems:
        return tid, "fail", "; ".join(p.splitlines()[0] for p in problems) + \
            ("\n" + "\n".join(problems[-1].splitlines()[1:]) if "\n" in problems[-1] else "")
    return tid, "ok", ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("selectors", nargs="*", help="task ids and/or domain names")
    ap.add_argument("--offline", action="store_true", help="skip tasks needing third-party deps")
    ap.add_argument("-j", type=int, default=4, help="parallel graders (default 4)")
    args = ap.parse_args()

    tasks = runner.discover()
    if not tasks:
        print("no tasks found"); sys.exit(1)
    if args.selectors:
        chosen = {}
        for sel in args.selectors:
            hits = {t: m for t, m in tasks.items()
                    if t == sel or t.split("/")[0] == sel}
            if not hits:
                hits = {runner.resolve(tasks, sel): tasks[runner.resolve(tasks, sel)]}
            chosen.update(hits)
        tasks = chosen
    if args.offline:
        skipped = [t for t, m in tasks.items() if m.get("deps")]
        tasks = {t: m for t, m in tasks.items() if not m.get("deps")}
        if skipped:
            print(DIM(f"--offline: skipping {len(skipped)} task(s) that need deps"))

    # Provision each unique dep-set once, serially, so parallel grading can't race.
    dep_sets = {tuple(sorted(m.get("deps", []))) for m in tasks.values()}
    for ds in sorted(dep_sets):
        runner.venv_for(list(ds))

    ok = fail = skip = 0
    failed = []
    with ThreadPoolExecutor(max_workers=args.j) as pool:
        for tid, verdict, detail in pool.map(lambda kv: selftest_one(*kv), sorted(tasks.items())):
            if verdict == "ok":
                print(f"  {GRN('✓')} {tid}"); ok += 1
            elif verdict == "skip":
                print(f"  {YEL('~')} {tid} {DIM(detail)}"); skip += 1
            else:
                print(f"  {RED('✗')} {tid}\n    {detail}"); fail += 1; failed.append(tid)
    print("----")
    print(f"verified: {ok}   problems: {fail}   skipped: {skip}")
    if failed:
        print("failed: " + " ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
