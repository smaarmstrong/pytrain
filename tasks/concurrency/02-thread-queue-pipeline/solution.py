import queue
import threading

_SENTINEL = object()


def run_pipeline(items, process, n_workers):
    q = queue.Queue()
    results = []
    results_lock = threading.Lock()

    def worker():
        while True:
            item = q.get()
            if item is _SENTINEL:
                q.task_done()
                return
            out = process(item)
            with results_lock:
                results.append(out)
            q.task_done()

    threads = [threading.Thread(target=worker) for _ in range(n_workers)]
    for t in threads:
        t.start()
    for item in items:
        q.put(item)
    for _ in threads:
        q.put(_SENTINEL)
    for t in threads:
        t.join()
    return results
