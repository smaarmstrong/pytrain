def dispatch(cmd) -> str:
    match cmd:
        case ("quit",):
            return "quit"
        case ("move", int() as x, int() as y) if x >= 0 and y >= 0:
            return f"move to ({x}, {y})"
        case ("move", _, _):
            return "invalid move"
        case ("line", (x1, y1), (x2, y2)):
            return f"line from ({x1}, {y1}) to ({x2}, {y2})"
        case {"action": "set", "key": key, "value": value}:
            return f"set {key}={value!r}"
        case [_, *_]:
            return f"sequence of {len(cmd)}"
        case str() as s:
            return f"text: {s}"
        case _:
            return "unknown"
