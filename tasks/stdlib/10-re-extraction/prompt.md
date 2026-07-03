# Pulling structure out of text

Four small extraction jobs for the `re` module. In `solution.py`:

```python
def parse_log_line(line):
    """Parse one log line of the exact shape

        "<YYYY-MM-DD> <LEVEL> <message>"

    e.g. "2024-03-10 ERROR disk full". LEVEL is one or more capital
    letters; the message is everything after the following space (at
    least one character, may itself contain spaces).

    Return {"date": ..., "level": ..., "message": ...} — or None if the
    line doesn't match the shape. (Named groups make this pleasant:
    match.groupdict().)
    """

def find_ints(text):
    """Every integer in `text`, as a list of ints, left to right.

    An integer is a maximal run of digits, optionally preceded by a minus
    sign: "t -3 x12" -> [-3, 12]. No numbers -> [].
    """

def int_spans(text):
    """The (start, end) index pairs of every integer found by find_ints,
    left to right — such that text[start:end] is the matched text.
    (This is what finditer gives you that findall can't.)
    """

def double_ints(text):
    """Replace every integer in `text` (same definition) with twice its
    value, leaving everything else untouched.

    "I own 3 cats and -2 dogs" -> "I own 6 cats and -4 dogs"
    Doing this in one pass needs re.sub with a FUNCTION as the
    replacement.
    """
```

Examples:

```python
>>> parse_log_line("2024-03-10 ERROR disk full")
{'date': '2024-03-10', 'level': 'ERROR', 'message': 'disk full'}
>>> parse_log_line("nonsense") is None
True
>>> find_ints("t -3 x12")
[-3, 12]
>>> int_spans("a 42 b 7")
[(2, 4), (7, 8)]
>>> double_ints("scores: 10, -4")
'scores: 20, -8'
```
