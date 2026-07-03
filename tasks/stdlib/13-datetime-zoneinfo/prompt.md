# Clocks, zones and one tricky flight

All inputs are fixed strings — never use the current time. Timestamps are
`"YYYY-MM-DD HH:MM"`, dates are `"YYYY-MM-DD"`, and time zones are IANA
names for `zoneinfo.ZoneInfo` (e.g. `"Europe/London"`). In `solution.py`:

```python
def parse_stamp(s):
    """'2024-03-10 14:30' -> the corresponding NAIVE datetime.datetime
    (tzinfo is None)."""

def to_utc(local_str, tz_name):
    """Interpret `local_str` as wall-clock time in `tz_name`; return an
    AWARE datetime expressing that same instant in UTC (utcoffset() is
    zero)."""

def flight_arrival(depart_str, depart_tz, minutes, arrive_tz):
    """A flight leaves at wall-clock `depart_str` in `depart_tz` and flies
    for `minutes` minutes. Return the arrival WALL-CLOCK time in
    `arrive_tz`, formatted 'YYYY-MM-DD HH:MM'.

    Beware: elapsed time is physical. Do the arithmetic on the instant
    (in UTC), not on local wall clocks — the grader schedules a flight
    across a DST jump, where local-clock arithmetic is an hour off.
    """

def days_between(d1, d2):
    """Calendar days from date-string d1 to d2: (d2 - d1) in days, as an
    int. Negative when d2 is earlier. Leap years must be right."""
```

Examples:

```python
>>> parse_stamp("2024-03-10 14:30")
datetime.datetime(2024, 3, 10, 14, 30)
>>> to_utc("2024-06-01 12:00", "Europe/London")   # BST is UTC+1
datetime.datetime(2024, 6, 1, 11, 0, tzinfo=datetime.timezone.utc)
>>> flight_arrival("2024-03-09 22:30", "America/New_York", 420, "Europe/London")
'2024-03-10 10:30'
>>> days_between("2024-01-31", "2024-03-01")      # 2024 is a leap year
30
```
