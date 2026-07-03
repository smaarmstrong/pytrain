from collections import Counter, defaultdict, deque


def word_counts(text):
    return Counter(text.lower().split())


def top_n(text, n):
    counts = word_counts(text)
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:n]


def group_by_length(words):
    groups = defaultdict(list)
    for w in words:
        groups[len(w)].append(w)
    return dict(groups)


def tail(iterable, n):
    return list(deque(iterable, maxlen=n)) if n > 0 else []
