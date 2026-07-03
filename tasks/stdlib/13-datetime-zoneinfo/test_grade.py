from datetime import datetime, timedelta, timezone

from pytrain_grader import load_solution, get_attr


def test_parse_stamp_naive():
    f = get_attr(load_solution(), "parse_stamp")
    got = f("2024-03-10 14:30")
    assert got == datetime(2024, 3, 10, 14, 30)
    assert got.tzinfo is None
    assert f("1999-12-31 23:59") == datetime(1999, 12, 31, 23, 59)


def test_to_utc_summer_and_winter_london():
    f = get_attr(load_solution(), "to_utc")
    summer = f("2024-06-01 12:00", "Europe/London")  # BST, UTC+1
    assert summer == datetime(2024, 6, 1, 11, 0, tzinfo=timezone.utc)
    assert summer.utcoffset() == timedelta(0)
    winter = f("2024-01-15 12:00", "Europe/London")  # GMT
    assert winter == datetime(2024, 1, 15, 12, 0, tzinfo=timezone.utc)


def test_to_utc_other_zones():
    f = get_attr(load_solution(), "to_utc")
    ny = f("2024-06-01 12:00", "America/New_York")  # EDT, UTC-4
    assert ny == datetime(2024, 6, 1, 16, 0, tzinfo=timezone.utc)
    tokyo = f("2024-06-01 12:00", "Asia/Tokyo")  # UTC+9, no DST
    assert tokyo == datetime(2024, 6, 1, 3, 0, tzinfo=timezone.utc)


def test_to_utc_crosses_midnight():
    f = get_attr(load_solution(), "to_utc")
    got = f("2024-06-01 01:30", "Asia/Tokyo")
    assert got == datetime(2024, 5, 31, 16, 30, tzinfo=timezone.utc)


def test_flight_arrival_transatlantic():
    f = get_attr(load_solution(), "flight_arrival")
    # NY 22:30 EST (UTC-5) = 03:30 UTC; +7h = 10:30 UTC; London still on GMT
    assert f("2024-03-09 22:30", "America/New_York", 420, "Europe/London") == "2024-03-10 10:30"


def test_flight_arrival_across_dst_jump():
    f = get_attr(load_solution(), "flight_arrival")
    # Departs 00:30 EST; US clocks spring forward at 02:00 on 2024-03-10.
    # 00:30 EST = 05:30 UTC; +2h = 07:30 UTC = 03:30 EDT.
    # Naive wall-clock arithmetic says 02:30 — an hour off.
    assert f("2024-03-10 00:30", "America/New_York", 120, "America/New_York") == "2024-03-10 03:30"


def test_flight_arrival_zero_minutes_pure_conversion():
    f = get_attr(load_solution(), "flight_arrival")
    # 12:00 Tokyo = 03:00 UTC = 04:00 London (BST)
    assert f("2024-06-01 12:00", "Asia/Tokyo", 0, "Europe/London") == "2024-06-01 04:00"


def test_days_between_leap_year():
    f = get_attr(load_solution(), "days_between")
    assert f("2024-01-31", "2024-03-01") == 30  # Feb 2024 has 29 days
    assert f("2023-01-31", "2023-03-01") == 29


def test_days_between_zero_and_negative():
    f = get_attr(load_solution(), "days_between")
    assert f("2024-06-01", "2024-06-01") == 0
    assert f("2024-03-01", "2024-01-31") == -30
