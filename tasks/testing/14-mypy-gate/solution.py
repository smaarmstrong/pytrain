"""Report helpers — typed until the mypy gate is green."""


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of empty data")
    return sum(values) / len(values)


def lookup(scores: dict[str, int], name: str, default: int | None = None) -> int | None:
    if name in scores:
        return scores[name]
    return default


def repeat(word: str, times: int = 2) -> str:
    return " ".join([word] * times)


def first_long_word(words: list[str], min_len: int) -> str | None:
    for word in words:
        if len(word) >= min_len:
            return word
    return None
