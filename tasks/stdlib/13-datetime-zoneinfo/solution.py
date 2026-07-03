from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

FMT = "%Y-%m-%d %H:%M"


def parse_stamp(s):
    return datetime.strptime(s, FMT)


def to_utc(local_str, tz_name):
    local = parse_stamp(local_str).replace(tzinfo=ZoneInfo(tz_name))
    return local.astimezone(timezone.utc)


def flight_arrival(depart_str, depart_tz, minutes, arrive_tz):
    depart_utc = to_utc(depart_str, depart_tz)
    arrive_utc = depart_utc + timedelta(minutes=minutes)
    return arrive_utc.astimezone(ZoneInfo(arrive_tz)).strftime(FMT)


def days_between(d1, d2):
    return (date.fromisoformat(d2) - date.fromisoformat(d1)).days
