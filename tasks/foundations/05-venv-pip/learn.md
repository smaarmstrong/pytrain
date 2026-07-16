THE IDEA

  Python comes with a big standard library ("batteries included"), but
  the wider ecosystem — pytest, requests, pandas — is THIRD-PARTY: you
  install those packages with a tool called pip.

  The catch: where do they get installed TO? If everything went into
  the one system-wide Python, every project on your machine would share
  one pile of packages — project A needs pandas 1.x, project B needs
  2.x, and upgrading for B silently breaks A.

  The fix is the VIRTUAL ENVIRONMENT (venv): a private, disposable
  Python-plus-packages folder, one per project. Install into the venv
  and only that project sees it. Delete the folder and it's as if it
  never happened. The whole modern Python workflow is:

      one project  ->  one venv  ->  pip install into it

---

WHY IT MATTERS

  You've already used this machinery without noticing: every time you
  `check` a task, this trainer builds (and caches) a venv containing
  pytest — that's why the first check said "provisioning venv..." and
  later ones didn't. Later domains (web, data) install real frameworks
  the same way. And the moment you start a project of your own, the
  first two commands you type are the ones below. Also: installing
  into the SYSTEM Python is how people break their operating system's
  tools — most Linux distros now refuse to even try
  ("externally-managed-environment" error). Venvs aren't optional
  etiquette; they're the paved road.

---

CREATE, ACTIVATE, INSTALL

  These are terminal commands, not Python, so run them in a shell —
  make a throwaway directory somewhere first (this is worth actually
  doing, it takes a minute):

      mkdir /tmp/venv-play && cd /tmp/venv-play

  1. CREATE — ask Python to build a venv in a folder named .venv:

         python3 -m venv .venv

     (`python3 -m venv` means "run the stdlib venv module as a
     program"; the trailing `.venv` is just the folder name — a dot
     name keeps it out of the way, and out of version control.)

  2. ACTIVATE — point THIS shell at the venv's Python:

         source .venv/bin/activate

     Your prompt grows a `(.venv)` prefix. That's the only magic:
     while active, `python3` and `pip` mean the venv's copies.
     (Windows: `.venv\Scripts\activate`.)

  3. INSTALL — fetch a package from PyPI (the Python Package Index)
     into the venv:

         pip install requests

     pip prints what it resolved and installed — requests plus the
     packages requests itself needs (its "dependencies").

  4. LOOK — two commands you'll use constantly:

         pip list                    # everything in this venv
         pip show requests           # details of one package

  5. LEAVE — done working:

         deactivate

     The venv still exists; activate it again any time. To destroy it,
     just delete the folder: `rm -rf .venv`. Nothing else on your
     machine changed — that's the point.

---

  How does Python know it's "in" a venv? Nothing global changed —
  activation just puts the venv first in your shell's PATH, so its
  interpreter is the one that runs. Python can report which
  interpreter is running and whether it's a venv:

```run
import sys
print(sys.executable)                       # the actual interpreter file
print(sys.prefix != sys.base_prefix)        # True inside a venv
```

  Run that here and you'll likely see False — the trainer's own runner
  uses your system Python (it needs nothing installed). Run the same
  two lines in the REPL inside your activated /tmp/venv-play venv and
  you'll see its .venv path and True. Same code, different
  environment — which is exactly the property venvs exist to give you.

---

ASKING PYTHON WHAT'S INSTALLED

  `pip list` is for humans at a shell. Code sometimes needs the same
  answer — "is package X here, and which version?" — and the standard
  library answers via importlib.metadata, which reads the records pip
  writes at install time:

```run
import importlib.metadata

# every installed distribution, programmatically (first few only):
names = sorted(d.metadata["Name"] for d in importlib.metadata.distributions())
print(len(names), "packages visible to this interpreter")
print(names[:5])
```

  And for one specific package there's version(), which either answers
  or raises a specific error:

```run
import importlib.metadata

try:
    print(importlib.metadata.version("pip"))
except importlib.metadata.PackageNotFoundError:
    print("pip isn't installed here")

try:
    print(importlib.metadata.version("surely-not-a-real-package"))
except importlib.metadata.PackageNotFoundError:
    print("surely-not-a-real-package isn't installed here")
```

  (Either line's answer depends on your system — some interpreters
  have pip, some don't. That's the lesson in miniature: "installed"
  is always a property of the ENVIRONMENT, never of Python itself.)
  That try/except around a specific exception type is the same
  expected-error pattern you used in the pytest lesson.

---

CHECK IT WORKED

  The task is the last snippet, packaged: installed_version(package)
  returns importlib.metadata.version(package), except that a missing
  package returns None instead of raising — so it's a try/except
  PackageNotFoundError with `return None` in the except branch.

  The grader runs your function inside one of the trainer's venvs,
  where pytest IS installed: it checks installed_version("pytest")
  matches the real version there, and that a made-up name gives None.

---

GOTCHAS

  - Forgot to activate? Then `pip install` goes to whatever Python
    your shell finds — possibly the system one (or fails with
    "externally-managed-environment"). The `(.venv)` prefix in your
    prompt is your seatbelt light; glance at it before installing.
  - One venv per PROJECT, not one big venv for everything — sharing
    one re-creates the very version conflicts venvs prevent.
  - Never commit the .venv folder to git; it's machine-specific and
    rebuildable. Recording what to install (requirements.txt,
    pyproject.toml) is the packaging domain's story.
  - "ModuleNotFoundError: No module named 'requests'" right after you
    installed it usually means two different Pythons: you installed
    into one and are running the other. `sys.executable` (above) is
    the truth serum.
  - The import name and the install name can differ: pip install
    beautifulsoup4, but import bs4. Check the package's docs when in
    doubt.
  - You may also meet `uv`, a fast modern replacement for the
    venv+pip pair (this trainer uses it when present). Same concepts,
    same folders — `uv venv`, `uv pip install` — so everything above
    transfers.
