# Plugin factory with a registry

In `solution.py`, implement a module-level plugin registry plus factory:

```python
def register(name): ...          # a decorator factory
def create(name, *args, **kwargs): ...
def registered_names(): ...
```

Behaviour:

- `@register("csv")` above a class adds that class to the registry under
  `"csv"` and returns the **class itself unchanged**, so it can still be
  used directly:

  ```python
  @register("csv")
  class CsvExporter:
      def __init__(self, path, delimiter=","): ...
  ```

- Registering a name that is already taken raises `ValueError` (the
  original registration survives).
- `create(name, *args, **kwargs)` looks the class up by name and returns a
  new instance, forwarding all positional and keyword arguments. An
  unregistered name raises `ValueError`.
- `registered_names()` returns a **sorted list** of all registered names.
- The registry starts empty: before anything is registered,
  `registered_names() == []` and every `create(...)` raises `ValueError`.

The grader registers its *own* classes — any class must be registrable,
not just ones you define.

Examples:

```python
>>> registered_names()
[]
>>> @register("json")
... class JsonExporter: ...
>>> isinstance(create("json"), JsonExporter)
True
>>> create("xml")
ValueError: ...
```
