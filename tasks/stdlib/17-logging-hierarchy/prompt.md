# Loggers that grow on trees

`logging.getLogger("app.audit")` is a **child** of `getLogger("app")`:
records propagate up the dotted hierarchy to ancestors' handlers. Your
functions log through named loggers; the grader attaches its own handler
to `"app"` and inspects what arrives. In `solution.py`:

```python
def audit(user, action):
    """Log an INFO record with message f"{user} did {action}" on the
    logger named "app.audit"."""

def warn_quota(user, pct):
    """Log on the logger named "app.quota":
    - pct >= 90:  a WARNING record, message f"{user} at {pct}%"
    - otherwise:  a DEBUG record, same message.
    """

def setup(stream):
    """Configure the "app" logger (and only it — don't touch the root
    logger):

    - attach a logging.StreamHandler writing to `stream`
    - give the handler a Formatter producing exactly
      "<LEVELNAME> <logger name>: <message>", i.e. the format string
      "%(levelname)s %(name)s: %(message)s"
    - set the "app" LOGGER's level to INFO (so DEBUG records are dropped,
      and INFO/WARNING from child loggers like app.audit flow up into
      the stream)

    Return the logger.
    """
```

After `setup(buf)`, `audit("ada", "login")` must append this line to
`buf`:

```
INFO app.audit: ada did login
```

…and `warn_quota("bob", 50)` must append nothing (DEBUG < INFO).
