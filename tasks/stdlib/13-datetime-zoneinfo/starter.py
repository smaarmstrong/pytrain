def parse_stamp(s):
    """'YYYY-MM-DD HH:MM' -> naive datetime."""
    raise NotImplementedError


def to_utc(local_str, tz_name):
    """Wall-clock time in tz_name -> the same instant as an aware UTC datetime."""
    raise NotImplementedError


def flight_arrival(depart_str, depart_tz, minutes, arrive_tz):
    """Arrival wall-clock 'YYYY-MM-DD HH:MM' in arrive_tz after `minutes` in the air."""
    raise NotImplementedError


def days_between(d1, d2):
    """(d2 - d1) in whole calendar days, as an int (negative if d2 earlier)."""
    raise NotImplementedError
