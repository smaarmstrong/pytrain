import pytest

from pytrain_grader import load_solution, get_attr


def test_hierarchy():
    mod = load_solution()
    ConfigError = get_attr(mod, "ConfigError")
    MissingKeyError_ = get_attr(mod, "MissingKeyError")
    InvalidValueError_ = get_attr(mod, "InvalidValueError")
    assert issubclass(ConfigError, Exception)
    assert issubclass(MissingKeyError_, ConfigError)
    assert issubclass(InvalidValueError_, ConfigError)


def test_parse_port_valid():
    f = get_attr(load_solution(), "parse_port")
    assert f("8080") == 8080
    assert f(443) == 443
    assert f("1") == 1
    assert f(65535) == 65535


def test_parse_port_unparseable_is_chained():
    mod = load_solution()
    f = get_attr(mod, "parse_port")
    InvalidValueError_ = get_attr(mod, "InvalidValueError")
    with pytest.raises(InvalidValueError_) as ei:
        f("abc")
    assert isinstance(ei.value.__cause__, ValueError), \
        "use `raise InvalidValueError(...) from <the ValueError>`"


def test_parse_port_out_of_range():
    mod = load_solution()
    f = get_attr(mod, "parse_port")
    InvalidValueError_ = get_attr(mod, "InvalidValueError")
    for bad in (0, -5, 65536, "70000"):
        with pytest.raises(InvalidValueError_):
            f(bad)


def test_parse_port_errors_catchable_as_configerror():
    mod = load_solution()
    f = get_attr(mod, "parse_port")
    ConfigError = get_attr(mod, "ConfigError")
    with pytest.raises(ConfigError):
        f("nope")


def test_get_port_success_path():
    mod = load_solution()
    f = get_attr(mod, "get_port")
    log = []
    assert f({"port": "80"}, log) == 80
    assert log == ["ok", "done"]


def test_get_port_missing_key():
    mod = load_solution()
    f = get_attr(mod, "get_port")
    MissingKeyError_ = get_attr(mod, "MissingKeyError")
    log = []
    with pytest.raises(MissingKeyError_):
        f({}, log)
    assert log == ["missing", "done"]


def test_get_port_invalid_value():
    mod = load_solution()
    f = get_attr(mod, "get_port")
    InvalidValueError_ = get_attr(mod, "InvalidValueError")
    log = []
    with pytest.raises(InvalidValueError_):
        f({"port": "not-a-port"}, log)
    assert log == ["invalid", "done"]
    assert "ok" not in log
