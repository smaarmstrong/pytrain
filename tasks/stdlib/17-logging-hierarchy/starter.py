def audit(user, action):
    """INFO f"{user} did {action}" on logger "app.audit"."""
    raise NotImplementedError


def warn_quota(user, pct):
    """WARNING (pct >= 90) or DEBUG f"{user} at {pct}%" on logger "app.quota"."""
    raise NotImplementedError


def setup(stream):
    """StreamHandler + '%(levelname)s %(name)s: %(message)s' formatter on "app";
    level INFO; return the logger."""
    raise NotImplementedError
