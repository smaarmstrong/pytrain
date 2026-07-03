import pytest

from pytrain_grader import load_solution, get_attr


class FakeDriver:
    """Grader's own driver honouring the awkward legacy interface."""

    def __init__(self, temp_raw="T=21.50C", hum_raw="H=45%"):
        self.temp_raw = temp_raw
        self.hum_raw = hum_raw
        self.connect_calls = 0
        self.connected = False

    def connect(self):
        self.connect_calls += 1
        self.connected = True

    def read_raw(self, channel):
        if not self.connected:
            raise RuntimeError("driver not connected")
        if channel == "TMP":
            return self.temp_raw
        if channel == "HUM":
            return self.hum_raw
        raise KeyError(channel)


def station_cls():
    return get_attr(load_solution(), "WeatherStation")


def test_temperature_is_a_float():
    st = station_cls()(FakeDriver())
    t = st.temperature()
    assert t == pytest.approx(21.5)
    assert isinstance(t, float)


def test_humidity_is_an_int():
    st = station_cls()(FakeDriver())
    h = st.humidity()
    assert h == 45
    assert isinstance(h, int)


def test_negative_and_other_values_parse():
    st = station_cls()(FakeDriver(temp_raw="T=-3.25C", hum_raw="H=100%"))
    assert st.temperature() == pytest.approx(-3.25)
    assert st.humidity() == 100


def test_constructor_does_not_connect():
    driver = FakeDriver()
    station_cls()(driver)
    assert driver.connect_calls == 0


def test_connects_lazily_and_at_most_once():
    driver = FakeDriver()
    st = station_cls()(driver)
    st.temperature()
    assert driver.connect_calls == 1
    st.humidity()
    st.temperature()
    st.humidity()
    assert driver.connect_calls == 1


def test_works_with_any_driver_shaped_object():
    class OtherDriver:
        def __init__(self):
            self.on = False

        def connect(self):
            self.on = True

        def read_raw(self, channel):
            if not self.on:
                raise RuntimeError("not connected")
            return {"TMP": "T=0.00C", "HUM": "H=7%"}[channel]

    st = station_cls()(OtherDriver())
    assert st.temperature() == pytest.approx(0.0)
    assert st.humidity() == 7


def test_malformed_readings_raise_valueerror():
    st = station_cls()(FakeDriver(temp_raw="banana", hum_raw="H=wet%"))
    with pytest.raises(ValueError):
        st.temperature()
    with pytest.raises(ValueError):
        st.humidity()
