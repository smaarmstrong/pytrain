from dataclasses import dataclass, field


@dataclass
class Book:
    title: str
    author: str
    pages: int = 0
    tags: list = field(default_factory=list)


@dataclass(frozen=True, order=True)
class Point:
    x: float
    y: float
