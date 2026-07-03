# Pin dependencies to a scenario

Your app (`app.py`, context only — don't change it) depends on two fictional
packages, `spanner` and `gearbox`. Nothing gets installed in this task: you
write version *constraints*, and the grader checks them logically against the
scenario below, the way a resolver would.

**The published versions**

| package | available versions |
|---|---|
| spanner | 1.0, 1.4, 1.5, 1.7.2, 2.0, 2.1 |
| gearbox | 0.9, 1.5, 1.6, 2.0 |

**The facts**

1. Your app uses a `spanner` feature that was **added in 1.5**.
2. Your app needs `gearbox` **1.5 or newer**.
3. `gearbox` 1.5 and 1.6 require `spanner < 2` (spanner 2.0 removed an API
   they use).
4. `gearbox` **2.0 has a critical bug** and must never be installed.

**Your job**: edit `constraints.txt` so it contains one PEP 508 requirement
line per package (comments starting with `#` and blank lines are fine), e.g.:

```
somepkg>=1.2,<2
```

A correct file allows *at least one* published version of each package, and
*only* versions consistent with all four facts. Exact pins (`==`) are
acceptable as long as they satisfy the scenario; ranges are more realistic.

The grader parses your file with `packaging.requirements`, computes which of
the published versions each of your constraints admits, and asserts the
admitted sets are non-empty and exclude every version the facts forbid.
