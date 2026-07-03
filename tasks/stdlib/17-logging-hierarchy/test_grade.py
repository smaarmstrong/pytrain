import io
import logging

import pytest

from pytrain_grader import load_solution, get_attr

LOGGERS = ["app", "app.audit", "app.quota"]


class Capture(logging.Handler):
    """The grader's own handler: collects LogRecords attached to 'app'."""

    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


@pytest.fixture(autouse=True)
def clean_loggers():
    def reset():
        for name in LOGGERS:
            lg = logging.getLogger(name)
            for h in list(lg.handlers):
                lg.removeHandler(h)
            lg.setLevel(logging.NOTSET)
            lg.propagate = True

    reset()
    yield
    reset()


@pytest.fixture()
def capture():
    cap = Capture()
    app = logging.getLogger("app")
    app.addHandler(cap)
    app.setLevel(logging.DEBUG)  # let everything through; we assert levels ourselves
    return cap


def test_audit_logs_info_on_app_audit(capture):
    audit = get_attr(load_solution(), "audit")
    audit("ada", "login")
    assert len(capture.records) == 1
    rec = capture.records[0]
    assert rec.name == "app.audit"
    assert rec.levelno == logging.INFO
    assert rec.getMessage() == "ada did login"


def test_audit_propagates_up_the_hierarchy(capture):
    # the capture handler sits on "app", NOT "app.audit" — records must
    # travel up the dotted-name tree to reach it
    audit = get_attr(load_solution(), "audit")
    audit("bob", "logout")
    assert [r.getMessage() for r in capture.records] == ["bob did logout"]


def test_warn_quota_high_is_warning(capture):
    warn_quota = get_attr(load_solution(), "warn_quota")
    warn_quota("eve", 95)
    warn_quota("mal", 90)  # boundary: >= 90
    assert [(r.name, r.levelno, r.getMessage()) for r in capture.records] == [
        ("app.quota", logging.WARNING, "eve at 95%"),
        ("app.quota", logging.WARNING, "mal at 90%"),
    ]


def test_warn_quota_low_is_debug(capture):
    warn_quota = get_attr(load_solution(), "warn_quota")
    warn_quota("bob", 50)
    (rec,) = capture.records
    assert rec.levelno == logging.DEBUG
    assert rec.getMessage() == "bob at 50%"


def test_setup_formats_records_into_the_stream():
    mod = load_solution()
    buf = io.StringIO()
    get_attr(mod, "setup")(buf)
    get_attr(mod, "audit")("ada", "login")
    assert buf.getvalue() == "INFO app.audit: ada did login\n"


def test_setup_level_info_drops_debug_keeps_warning():
    mod = load_solution()
    buf = io.StringIO()
    get_attr(mod, "setup")(buf)
    get_attr(mod, "warn_quota")("bob", 50)  # DEBUG -> dropped
    assert buf.getvalue() == ""
    get_attr(mod, "warn_quota")("eve", 95)  # WARNING -> kept
    assert buf.getvalue() == "WARNING app.quota: eve at 95%\n"


def test_setup_returns_the_app_logger_and_spares_root():
    mod = load_solution()
    root_handlers_before = list(logging.getLogger().handlers)
    got = get_attr(mod, "setup")(io.StringIO())
    assert got is logging.getLogger("app")
    assert logging.getLogger().handlers == root_handlers_before
