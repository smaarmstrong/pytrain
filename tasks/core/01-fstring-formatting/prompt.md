# Receipt strings

Four tiny string-building functions in `solution.py`. Each is a one-line
f-string once you know the format spec mini-language.

```python
def receipt_line(item: str, price: float) -> str:
    """`item` left-aligned in a field of 12, then '£', then `price`
    right-aligned in a field of 8 with a thousands separator and exactly
    2 decimal places."""

def percent(fraction: float) -> str:
    """A fraction (0.256) rendered as a percentage with 1 decimal
    place: '25.6%'."""

def debug_line(name: str, value) -> str:
    """Mimic f-string `=` debugging output: the name, '=', then the
    *repr* of the value. debug_line('user', 'bo') == "user='bo'"."""

def quoted(name: str, nickname: str) -> str:
    """'<name> is called "<nickname>"' — the nickname in double quotes.
    quoted('Bo', 'Ace') == 'Bo is called "Ace"'."""
```

Behaviour details:

- `receipt_line("widget", 1234.5)` → `'widget      £1,234.50'`
  (item padded to 12 chars; `1,234.50` is exactly 8 chars, shorter prices
  are right-aligned with spaces: `receipt_line("tea", 3.5)` →
  `'tea         £    3.50'`).
- `percent(1.0)` → `'100.0%'`, `percent(0.005)` → `'0.5%'`.
- `debug_line("n", 42)` → `'n=42'` — note repr, so strings keep quotes.
- No trailing whitespace beyond what the field widths produce.

Examples:

```python
>>> receipt_line("widget", 1234.5)
'widget      £1,234.50'
>>> percent(0.256)
'25.6%'
>>> debug_line("user", "bo")
"user='bo'"
>>> quoted("Bo", "Ace")
'Bo is called "Ace"'
```
