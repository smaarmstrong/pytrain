import re

LOG_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2}) (?P<level>[A-Z]+) (?P<message>.+)$"
)
INT_RE = re.compile(r"-?\d+")


def parse_log_line(line):
    m = LOG_RE.match(line)
    return m.groupdict() if m else None


def find_ints(text):
    return [int(s) for s in INT_RE.findall(text)]


def int_spans(text):
    return [m.span() for m in INT_RE.finditer(text)]


def double_ints(text):
    return INT_RE.sub(lambda m: str(int(m.group()) * 2), text)
