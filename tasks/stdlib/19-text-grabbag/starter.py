def wrap(text, width):
    """Greedy word-wrap into a list of lines of at most `width` chars."""
    raise NotImplementedError


def dedent(text):
    """Remove the common leading whitespace from every line."""
    raise NotImplementedError


def render(template, mapping):
    """string.Template safe substitution: unknown placeholders left intact."""
    raise NotImplementedError


def token(n):
    """n secrets-random characters from ASCII letters + digits."""
    raise NotImplementedError
