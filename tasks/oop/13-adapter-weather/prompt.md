# Adapter: taming a legacy sensor driver

You must integrate an awkward legacy driver you cannot change. Every driver
object exposes exactly this interface:

- `driver.connect()` — must be called before any read; reads before it
  raise `RuntimeError`.
- `driver.read_raw(channel)` — returns awkward raw strings:
  - channel `"TMP"` → `"T=<number>C"`, e.g. `"T=21.50C"` or `"T=-3.25C"`;
  - channel `"HUM"` → `"H=<integer>%"`, e.g. `"H=45%"`.

(`starter.py` ships a sample `LegacyDriver` you can play with; the grader
substitutes its own driver objects with the same interface.)

In `solution.py`, write the **adapter**:

```python
class WeatherStation:
    def __init__(self, driver): ...
    def temperature(self): ...
    def humidity(self): ...
```

Behaviour:

- The driver is *injected* — `WeatherStation` works with any object
  honouring the interface above.
- `temperature()` returns the temperature as a `float` (`21.5`, `-3.25`).
- `humidity()` returns the humidity as an `int` (`45`).
- Connection management is the adapter's job, hidden from callers:
  - the constructor must **not** call `connect()`;
  - `connect()` is called lazily on the first read, and **at most once**
    ever, no matter how many reads follow (the grader counts).
- If the driver returns a string not matching the formats above, raise
  `ValueError`.

Examples:

```python
>>> station = WeatherStation(LegacyDriver())
>>> station.temperature()
21.5
>>> station.humidity()
45
```
