def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item


def chunk_sum(chunk):
    total = 0
    for x in chunk:
        yield x
        total += x
    return total


def stream_sums(chunks):
    sums = []
    for chunk in chunks:
        sums.append((yield from chunk_sum(chunk)))
    return sums
