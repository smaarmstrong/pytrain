from dataclasses import dataclass, field, fields
from typing import Any, get_type_hints

# TODO: @dataclass class Task ...


def field_types(cls):
    raise NotImplementedError


def mismatched_fields(obj):
    raise NotImplementedError
