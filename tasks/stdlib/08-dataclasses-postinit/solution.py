import hashlib
from dataclasses import InitVar, dataclass, field


@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")
        self.area = self.width * self.height


@dataclass
class User:
    name: str
    password: InitVar[str]
    password_hash: str = field(init=False)

    def __post_init__(self, password):
        self.password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()


def check(user, attempt):
    return hashlib.sha256(attempt.encode("utf-8")).hexdigest() == user.password_hash
