# Dataclasses meet get_type_hints

Annotations drive dataclasses at runtime — and `typing.get_type_hints` lets
*you* read them back, with string annotations resolved to real types. In
`solution.py`:

1. A dataclass:

```python
@dataclass
class Task:
    title: str
    priority: int = 1
    tags: list[str] = field(default_factory=list)
    done: bool = False
```

2. Two introspection helpers (they must work on ANY class/instance, not just
   `Task` — including classes whose annotations are strings, so use
   `typing.get_type_hints`, not raw `__annotations__`):

```python
def field_types(cls: type) -> dict[str, type]:
    """Mapping of annotated attribute name -> RESOLVED type for cls.
    E.g. an attribute annotated "int" (a string) maps to the int class."""

def mismatched_fields(obj: Any) -> list[str]:
    """For a dataclass INSTANCE: the names of fields whose current value is
    not an instance of the field's resolved annotated type, sorted
    alphabetically. Only check fields whose resolved hint is a plain class
    (isinstance(hint, type)); skip parametrised hints like list[str].
    Checks use isinstance (so a bool value is fine for an int field)."""
```

Examples:

```python
>>> t = Task("write docs")
>>> t.priority, t.tags, t.done
(1, [], False)
>>> field_types(Task) == {'title': str, 'priority': int, 'tags': list[str], 'done': bool}
True
>>> mismatched_fields(Task(title=123))          # doctest-ish: title should be str
['title']
>>> mismatched_fields(Task("ok"))
[]
```

The grader also checks that two `Task()` instances don't share the same
`tags` list (that's what `default_factory` is for) and that dataclass
equality works (`Task("a") == Task("a")`).
