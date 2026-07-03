"""A correct implementation of the spec in prompt.md — write tests for it."""


def encode(s):
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch:
            pairs[-1] = (ch, pairs[-1][1] + 1)
        else:
            pairs.append((ch, 1))
    return pairs


def decode(pairs):
    return "".join(ch * count for ch, count in pairs)
