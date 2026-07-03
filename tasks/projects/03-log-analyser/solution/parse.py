"""Line-parsing layer: one compiled regex for the Common Log Format."""
import re

LINE_RE = re.compile(
    r'^(?P<ip>\S+) (?P<ident>\S+) (?P<user>\S+) '
    r'\[(?P<timestamp>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]*)" '
    r'(?P<status>\d{3}) (?P<size>\d+|-)$'
)


def parse_line(line):
    """Dict for a well-formed line, None for a malformed one."""
    m = LINE_RE.match(line.rstrip("\n"))
    if m is None:
        return None
    rec = m.groupdict()
    rec["status"] = int(rec["status"])
    rec["size"] = 0 if rec["size"] == "-" else int(rec["size"])
    return rec
