class EventBus:
    """Observer pattern: subscribe/unsubscribe callables per event name;
    publish(event, payload) fans the payload out in subscription order."""

    def subscribe(self, event, callback):
        raise NotImplementedError

    def unsubscribe(self, event, callback):
        raise NotImplementedError

    def publish(self, event, payload):
        raise NotImplementedError
