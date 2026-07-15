THE IDEA

  An exception is Python's way of signalling "something went wrong" — it
  stops normal flow and travels up until some code catches it. Exceptions
  are just objects, arranged in a family tree by inheritance. You can make
  your OWN by subclassing, and that tree is what lets a caller catch a whole
  category at once.

---

  You define a new exception type by inheriting from an existing one. A base
  class plus two children that ARE-A base:

```run
class ConfigError(Exception): pass
class MissingKeyError(ConfigError): pass
class InvalidValueError(ConfigError): pass

# Because both inherit from ConfigError, catching the base catches either:
try:
    raise MissingKeyError("no port")
except ConfigError as e:
    print("caught as ConfigError:", type(e).__name__)
```

  That is the payoff of a hierarchy: a caller who writes
  `except ConfigError` handles every configuration problem without listing
  each subclass. That is the class part of this task done.

---

WHY IT MATTERS

  Real systems distinguish KINDS of failure — a missing setting versus a
  malformed one deserve different messages or recovery. A small exception
  hierarchy gives callers that choice (catch one specific type, or the whole
  family) instead of parsing error strings. It's how well-built libraries
  report trouble.

---

RAISING, AND CHAINING WITH `from`

  When you catch a low-level error and raise a friendlier one, you can keep
  the original attached as the "cause" with `raise NewError(...) from
  original`. Python records it on the new error's `__cause__`:

```run
class InvalidValueError(Exception): pass

def parse_port(raw):
    try:
        port = int(raw)                       # raises ValueError on "abc"
    except ValueError as e:
        raise InvalidValueError(f"not an int: {raw!r}") from e

try:
    parse_port("abc")
except InvalidValueError as e:
    print(e)
    print("caused by:", repr(e.__cause__))    # the original ValueError
```

  The `from e` is what the grader inspects — it links your clean error back
  to the raw cause, so a debugger can see the full story.

---

  The rest of `parse_port` is a plain range check. `int("8080")` gives 8080;
  if it's outside 1..65535, raise InvalidValueError (no chaining needed
  there — nothing lower-level failed, the value is simply wrong).

---

try / except / else / finally

  A try block has up to four parts, and the last two are the subtle ones:

    try:      code that might fail
    except:   runs only if a matching error happened
    else:     runs only if NO exception happened
    finally:  runs ALWAYS — success or failure, even if the error re-raises

```run
def demo(x):
    log = []
    try:
        if x < 0:
            raise ValueError("negative")
    except ValueError:
        log.append("failed")
    else:
        log.append("ok")           # only when the try succeeded
    finally:
        log.append("done")         # every time, last
    return log

print(demo(5))                     # ['ok', 'done']
print(demo(-1))                    # ['failed', 'done']
```

  Notice "done" is last in BOTH cases, and "ok" appears only on success.
  That is exactly the audit-trail shape `get_port` must produce.

---

  One more tool: `raise ... from None` SUPPRESSES chaining. In `get_port`,
  when the key is missing you catch the KeyError but don't want it cluttering
  the trace — you raise MissingKeyError `from None` to present a clean error.

---

CHECK IT WORKED

  The pieces:

    the three classes  ->  subclass Exception, then ConfigError; catchable
                           as ConfigError because they inherit it
    parse_port         ->  int() in a try; on failure raise InvalidValueError
                           `from e`; then a 1..65535 range check
    get_port           ->  look up "port" (missing -> log "missing", raise
                           MissingKeyError from None); parse (fail -> log
                           "invalid", re-raise); else log "ok" and return;
                           finally log "done"

  The grader reads the log list AND checks `__cause__`, so both the ordering
  and the chaining have to be right.

---

GOTCHAS

  - `else` runs only when the try body raised nothing — that's how "ok" is
    kept out of the log on failure. Putting the append in the try body
    instead would log "ok" even when a later line fails.
  - `finally` always runs, so "done" is guaranteed last — even while an
    exception is on its way up and out of the function.
  - `from e` attaches the cause; `from None` hides it. The task uses both,
    deliberately, in different spots.
  - A bare `raise` inside an except block re-raises the SAME exception,
    preserving its type and traceback — that's what "invalid" re-raise wants.
