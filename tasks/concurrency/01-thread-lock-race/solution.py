import threading


def increment_many(probe, lock, times):
    for _ in range(times):
        with lock:
            probe.write(probe.read() + 1)


def run_workers(probe, lock, n_threads, times_per_thread):
    threads = [
        threading.Thread(target=increment_many, args=(probe, lock, times_per_thread))
        for _ in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return probe.read()
