# Lazy quantifiers and lookarounds

Two regex superpowers that separate the fluent from the frustrated:
`*?`/`+?` (lazy — match as LITTLE as possible) and
`(?=...)`/`(?<=...)` (lookarounds — assert without consuming). In
`solution.py`:

```python
def bold_texts(html):
    """The contents of every <b>...</b> pair, in order.

    A greedy ".*" would swallow from the first <b> to the LAST </b>;
    you must not: bold_texts("<b>a</b> and <b>b</b>") == ["a", "b"].
    Contents never contain "<". No pairs -> [].
    """

def quoted(text):
    """Every double-quoted string in `text`, in order, quotes stripped.

    quoted('say "hi" then "bye"') == ["hi", "bye"] — again, the shortest
    match between quotes, never across them. Quoted parts never contain
    escaped quotes. None -> [].
    """

def dollar_amounts(text):
    """Every number directly preceded by a "$", WITHOUT the "$", as a
    list of ints. Numbers not preceded by $ are ignored.

    dollar_amounts("pay $30 or 40 or $5") == [30, 5]
    A lookbehind keeps the "$" out of the match.
    """

def split_camel(name):
    """Insert a single space at every lower-to-UPPER boundary.

    split_camel("parseHTTPResponse") -> "parse HTTPResponse"
    split_camel("camelCaseName")     -> "camel Case Name"
    split_camel("simple")            -> "simple"

    The trick: a zero-width pattern made of a lookbehind for [a-z]
    followed by a lookahead for [A-Z] — it consumes NOTHING, so re.sub
    can replace it with a space without eating letters.
    """
```

Examples:

```python
>>> bold_texts("x <b>one</b> y <b>two</b>")
['one', 'two']
>>> quoted('a "b" c')
['b']
>>> dollar_amounts("$7 then 8 then $9")
[7, 9]
>>> split_camel("aB")
'a B'
```
