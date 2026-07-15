THE IDEA

  When you write a name in Python — `x`, `count`, `prefix` — the interpreter
  has to decide WHICH x you mean. It looks in four places, in order, and
  stops at the first hit. The initials spell LEGB:

    L  Local      names defined inside the current function
    E  Enclosing  names in a function that wraps this one
    G  Global     names at the top level of the module (the file)
    B  Built-in   names Python always provides (len, print, range, ...)

  Most bugs in this area come from being surprised about which scope a name
  lives in, or from a default value that is shared when you thought it was
  fresh. This lesson walks through all three cases in the task.

---

THE MUTABLE-DEFAULT TRAP

  Here is one of Python's most famous gotchas. A default value is created
  ONCE, when the function is defined — not fresh on each call. So a default
  list is shared by every call that uses it:

```run
def buggy(item, items=[]):         # DON'T do this
    items.append(item)
    return items

print(buggy(1))                    # [1]
print(buggy(2))                    # [1, 2]  <-- the list persisted!
```

  See how the second call still had the 1 in it? That one list is reused
  across calls. Almost never what you want.

---

  The fix is a fixed idiom: default to None, and make a fresh list inside the
  function when None was passed:

```run
def append_item(item, items=None):
    if items is None:
        items = []                 # a brand-new list, this call only
    items.append(item)
    return items

print(append_item(1))              # [1]
print(append_item(2))              # [2]  <-- independent, as it should be
```

  And when the caller DOES pass a list, `items is None` is false, so you
  mutate and return their exact list — which is the behaviour the task asks
  for. That is `append_item` done.

---

GLOBAL: rebinding a module-level name

  A function can READ a global name freely. But if it wants to REASSIGN one,
  it must say so with the `global` statement — otherwise Python assumes any
  name you assign to is a new local, and you'd get an error:

```run
_counter = 0                       # lives at module (global) level

def next_id():
    global _counter                # "I mean the module-level one"
    _counter += 1                  # rebind it
    return _counter

print(next_id(), next_id(), next_id())   # 1 2 3
```

  Without the `global` line, `_counter += 1` would try to read a local
  `_counter` that doesn't exist yet and raise UnboundLocalError. The
  `global` keyword is what lets independent callers share one counter.

---

ENCLOSING: a closure remembers its surroundings

  A function defined INSIDE another can see the outer function's variables,
  and it keeps seeing them even after the outer function has returned. That
  captured-variable function is called a "closure":

```run
def make_prefixer(prefix):
    def prefixer(s):
        return prefix + s          # `prefix` comes from the enclosing scope
    return prefixer

shout = make_prefixer(">> ")
whisper = make_prefixer(".. ")
print(shout("hi"))                 # >> hi
print(whisper("hi"))               # .. hi
```

  Each call to make_prefixer gets its OWN `prefix`, so `shout` and `whisper`
  don't interfere — that independence is exactly what the task checks.

---

CHECK IT WORKED

  Three functions, three scopes:

    append_item   ->  default None, make a fresh [] inside (avoid the trap)
    next_id       ->  a module-level counter + the `global` statement
    make_prefixer ->  return an inner function that closes over `prefix`

  The grader interleaves calls (two prefixers at once, repeated next_id) to
  prove nothing is accidentally shared that shouldn't be, and that the one
  thing that SHOULD be shared (the counter) is.

---

GOTCHAS

  - Never use a mutable default (`[]`, `{}`, `set()`). Default to None and
    build it inside. This is the single most important habit here.
  - `global` is only needed to REASSIGN a global. Reading one, or mutating a
    global list with .append(), needs no declaration.
  - A closure captures the VARIABLE, not a snapshot — fine here because each
    make_prefixer call has its own separate `prefix`.
  - `is None` is the right test, not `if not items:` — an empty list the
    caller passed on purpose is falsy too, and you'd wrongly replace it.
