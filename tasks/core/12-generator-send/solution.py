def chunks(items, size):
    if size < 1:
        raise ValueError("size must be >= 1")
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def averager():
    total = 0.0
    count = 0
    mean = None
    while True:
        value = yield mean
        total += value
        count += 1
        mean = total / count
