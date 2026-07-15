THE IDEA

  This task is about two related ideas that both use * and **:

    1. UNPACKING — pulling a sequence apart into named pieces.
    2. PARAMETER KINDS — controlling how a function may be called.

  We'll take them one at a time; neither is hard once named.

---

UNPACKING: giving several names at once

  Python lets you assign to several names in one go by matching shape:

```run
first, last = ("a", "b")
print(first, last)                 # a b
```

  The right side had two items, so we gave two names. But what if you don't
  know how many items are in the middle?

---

STARRED assignment: one name soaks up the rest

  Put a * on one name and it becomes a list of "everything left over", while
  the plain names still grab one item each:

```run
first, *middle, last = [1, 2, 3, 4]
print(first)                       # 1
print(middle)                      # [2, 3, 4] ... wait, read on
print(last)                        # 4
```

  Look carefully: `first` took the first item, `last` took the last, and the
  starred `middle` collected EVERYTHING between them into a list. With only
  two items there's nothing in between, so middle is empty:

```run
first, *middle, last = "ab"
print(first, middle, last)         # a [] b
```

  That single line is the whole of `head_tail` — you just need to raise a
  ValueError first when there are fewer than two items to split.

---

  Raising an error is one statement. `raise` followed by the error you want:

```run
def head_tail(seq):
    if len(seq) < 2:
        raise ValueError("need at least two items")
    first, *middle, last = seq
    return first, middle, last

print(head_tail([1, 2, 3, 4]))     # (1, [2, 3], 4)
```

---

* AND ** IN FUNCTION PARAMETERS

  The same symbols, on a function's parameters, mean "collect extra
  arguments". `*dicts` gathers extra POSITIONAL arguments into a tuple;
  `**overrides` gathers extra KEYWORD arguments into a dict:

```run
def show(*args, **kwargs):
    print("positional:", args)
    print("keyword:   ", kwargs)

show({"a": 1}, {"b": 2}, port=8080, debug=True)
```

  So `merge(*dicts, **overrides)` receives every dict you pass as a tuple,
  and every `key=value` as a dict — you just merge them in order (later
  wins), building a NEW dict so you never mutate the caller's data.

---

PARAMETER KINDS: `/` and `*` as separators

  Sometimes you want to control HOW a parameter may be passed. Two special
  markers in the parameter list do this:

    everything BEFORE a  /  is positional-only  (can't be named in the call)
    everything AFTER  a  *  is keyword-only      (must be named in the call)

```run
def clamp(value, /, lo, hi, *, strict=False):
    return max(lo, min(hi, value))

print(clamp(15, 0, 10))            # 10  — fine
print(clamp(15, lo=0, hi=10))      # 10  — lo/hi may be named
```

  Because `value` is before the `/`, calling `clamp(value=5, ...)` is a
  TypeError — you declared it positional-only, so Python enforces it; you
  don't write that check yourself. Because `strict` is after the `*`, it can
  only be given as `strict=True`, never positionally.

---

CHECK IT WORKED

  Putting the pieces together:

    head_tail  ->  guard with ValueError, then  first, *middle, last = seq
    merge      ->  start {}, .update() each dict, then .update(overrides)
    clamp      ->  the signature does the enforcing; body clamps, and with
                   strict=True raises ValueError when value is out of range

  The grader deliberately makes bad calls (naming a positional-only arg,
  passing a keyword-only one positionally) and expects the TypeError Python
  raises for you — so getting the signature right is most of the task.

---

GOTCHAS

  - Only ONE starred name is allowed per unpacking (Python can't tell where
    two greedy collectors would split).
  - `*` gathers positionals into a tuple; `**` gathers keywords into a dict.
    Don't swap them.
  - Let Python raise the TypeError for wrong call styles — declaring the
    parameter kind IS the check. Writing your own is both extra work and
    the wrong error type.
  - merge must return a fresh dict. Start from {} and update into it; never
    update the first argument in place.
