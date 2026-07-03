# Overloading a polymorphic function

`double` means different things for different inputs — and each input type has
its own return type. A single union signature (`int | str | list[int]` in,
`int | str | list[int]` out) loses the connection between them; that's what
`@typing.overload` is for.

In `solution.py`, write `double` with **three overload declarations** plus the
real implementation:

```python
@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
@overload
def double(x: list[int]) -> list[int]: ...
def double(x):        # the implementation (may be annotated more loosely)
    ...
```

Behaviour:

- `double(3) == 6`
- `double("ab") == "abab"`
- `double([1, 2]) == [2, 4]` — a NEW list, each element doubled (not the
  list repeated!), input unchanged; `double([]) == []`.

Grading: behaviour as above, plus the grader calls
`typing.get_overloads(double)` (the runtime registry `@typing.overload` fills
in on 3.11+) and checks the three declared input->return type pairings:
`int -> int`, `str -> str`, `list[int] -> list[int]`.
