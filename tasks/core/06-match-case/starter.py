def dispatch(cmd) -> str:
    """Interpret one drawing command (see prompt.md for the rule table).

    Intended as a single match statement:

        match cmd:
            case ("quit",):
                ...
    """
    raise NotImplementedError
