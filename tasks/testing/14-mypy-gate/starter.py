"""Report helpers — fully working, completely untyped.

Annotate until the mypy command in the prompt reports no errors.
Do not change any runtime behaviour.
"""


def mean(values):
    if not values:
        raise ValueError("mean of empty data")
    return sum(values) / len(values)


def lookup(scores, name, default=None):
    if name in scores:
        return scores[name]
    return default


def repeat(word, times=2):
    return " ".join([word] * times)


def first_long_word(words, min_len):
    for word in words:
        if len(word) >= min_len:
            return word
    return None
