class EventBus:
    def __init__(self):
        self._subscribers = {}  # event -> list of callbacks, in order

    def subscribe(self, event, callback):
        callbacks = self._subscribers.setdefault(event, [])
        if callback in callbacks:
            raise ValueError(f"already subscribed to {event!r}")
        callbacks.append(callback)

    def unsubscribe(self, event, callback):
        callbacks = self._subscribers.get(event, [])
        if callback not in callbacks:
            raise ValueError(f"not subscribed to {event!r}")
        callbacks.remove(callback)

    def publish(self, event, payload):
        callbacks = list(self._subscribers.get(event, []))
        for callback in callbacks:
            callback(payload)
        return len(callbacks)
