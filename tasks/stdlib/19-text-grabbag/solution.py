import secrets
import string
import textwrap

ALPHABET = string.ascii_letters + string.digits


def wrap(text, width):
    return textwrap.wrap(text, width)


def dedent(text):
    return textwrap.dedent(text)


def render(template, mapping):
    return string.Template(template).safe_substitute(mapping)


def token(n):
    return "".join(secrets.choice(ALPHABET) for _ in range(n))
