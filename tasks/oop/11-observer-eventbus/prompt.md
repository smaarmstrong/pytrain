# EventBus: observer / pub-sub

In `solution.py`, implement a publish/subscribe event bus:

```python
class EventBus:
    def subscribe(self, event, callback): ...
    def unsubscribe(self, event, callback): ...
    def publish(self, event, payload): ...
```

Behaviour:

- `subscribe(event, callback)` registers a callable for a (string) event
  name. Subscribing the *same* callback to the *same* event twice raises
  `ValueError` (it stays subscribed once). The same callback may subscribe
  to several different events.
- `publish(event, payload)` calls every callback currently subscribed to
  that event as `callback(payload)`, **in subscription order**, and returns
  the number of callbacks invoked. Publishing an event nobody subscribed to
  is fine: no error, returns `0`. Subscribers of *other* events are never
  called.
- `unsubscribe(event, callback)` removes the registration; that callback is
  not called by later publishes of that event (registrations for other
  events are untouched). Unsubscribing a callback that isn't subscribed to
  that event raises `ValueError`.

Examples:

```python
>>> bus = EventBus()
>>> seen = []
>>> bus.subscribe("order.created", seen.append)
>>> bus.publish("order.created", {"id": 1})
1
>>> seen
[{'id': 1}]
>>> bus.unsubscribe("order.created", seen.append)
>>> bus.publish("order.created", {"id": 2})
0
```
