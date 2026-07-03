# Wrap, dedent, template, token

Four one-screen text utilities from `textwrap`, `string` and `secrets`.
In `solution.py`:

```python
def wrap(text, width):
    """Wrap `text` into a list of lines, each at most `width` characters.

    Words (whitespace-separated; each is guaranteed <= width) are never
    split, their order is preserved, words on a line are joined by a
    single space, and packing is GREEDY: a word goes on the current line
    whenever it fits. Empty/whitespace-only text -> [].
    (textwrap.wrap does exactly this.)
    """

def dedent(text):
    """Strip the longest common leading whitespace from every line, like
    textwrap.dedent. Empty lines don't count towards (or against) the
    common prefix. Relative indentation survives:

    dedent("    a\\n      b\\n") == "a\\n  b\\n"
    """

def render(template, mapping):
    """Substitute string.Template placeholders ($name or ${name}) from
    `mapping` — leaving UNKNOWN placeholders exactly as written (that's
    safe_substitute, not substitute). "$$" renders as a literal "$".
    """

def token(n):
    """A random token: exactly `n` characters, each drawn from ASCII
    letters + digits, chosen with the cryptographic `secrets` module
    (not `random`). token(0) == "".
    """
```

Examples:

```python
>>> wrap("the quick brown fox jumps", 10)
['the quick', 'brown fox', 'jumps']
>>> dedent("    a\n      b\n")
'a\n  b\n'
>>> render("$name is ${age}", {"name": "Ada"})
'Ada is ${age}'
>>> len(token(16)), token(3) == token(3)
(16, False)
```
