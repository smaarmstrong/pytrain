import re


class LegacyDriver:
    """The awkward interface being adapted (sample implementation)."""

    def __init__(self):
        self._connected = False

    def connect(self):
        self._connected = True

    def read_raw(self, channel):
        if not self._connected:
            raise RuntimeError("driver not connected")
        if channel == "TMP":
            return "T=21.50C"
        if channel == "HUM":
            return "H=45%"
        raise KeyError(channel)


class WeatherStation:
    def __init__(self, driver):
        self._driver = driver
        self._connected = False

    def _ensure_connected(self):
        if not self._connected:
            self._driver.connect()
            self._connected = True

    def temperature(self):
        self._ensure_connected()
        raw = self._driver.read_raw("TMP")
        m = re.fullmatch(r"T=(-?\d+(?:\.\d+)?)C", raw)
        if not m:
            raise ValueError(f"malformed temperature reading: {raw!r}")
        return float(m.group(1))

    def humidity(self):
        self._ensure_connected()
        raw = self._driver.read_raw("HUM")
        m = re.fullmatch(r"H=(-?\d+)%", raw)
        if not m:
            raise ValueError(f"malformed humidity reading: {raw!r}")
        return int(m.group(1))
