class LegacyDriver:
    """The awkward interface you must adapt (do not modify).

    The grader uses its own drivers with this same interface — program
    against the interface, not this particular class.
    """

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
    """Adapter: clean temperature()/humidity() over the legacy driver.

    Must connect lazily (not in __init__) and at most once — see prompt.md.
    """

    def __init__(self, driver):
        raise NotImplementedError

    def temperature(self):
        raise NotImplementedError

    def humidity(self):
        raise NotImplementedError
