import pytest

from pytrain_grader import load_solution, get_attr


def make_bus():
    return get_attr(load_solution(), "EventBus")()


def test_subscriber_receives_payload():
    bus = make_bus()
    seen = []
    bus.subscribe("order.created", seen.append)
    bus.publish("order.created", {"id": 1})
    assert seen == [{"id": 1}]


def test_publish_returns_number_of_callbacks_invoked():
    bus = make_bus()
    bus.subscribe("e", lambda p: None)
    bus.subscribe("e", lambda p: None)
    assert bus.publish("e", "x") == 2
    assert bus.publish("nobody-home", "x") == 0


def test_callbacks_run_in_subscription_order():
    bus = make_bus()
    order = []
    bus.subscribe("e", lambda p: order.append("first"))
    bus.subscribe("e", lambda p: order.append("second"))
    bus.subscribe("e", lambda p: order.append("third"))
    bus.publish("e", None)
    assert order == ["first", "second", "third"]


def test_other_events_do_not_leak():
    bus = make_bus()
    a, b = [], []
    bus.subscribe("a", a.append)
    bus.subscribe("b", b.append)
    bus.publish("a", 1)
    assert a == [1]
    assert b == []


def test_unsubscribed_callback_is_not_called():
    bus = make_bus()
    gone, kept = [], []
    bus.subscribe("e", gone.append)
    bus.subscribe("e", kept.append)
    bus.unsubscribe("e", gone.append)
    assert bus.publish("e", 42) == 1
    assert gone == []
    assert kept == [42]


def test_duplicate_subscribe_raises_and_keeps_single_registration():
    bus = make_bus()
    seen = []
    bus.subscribe("e", seen.append)
    with pytest.raises(ValueError):
        bus.subscribe("e", seen.append)
    bus.publish("e", "once")
    assert seen == ["once"]


def test_unsubscribe_unknown_raises_valueerror():
    bus = make_bus()
    cb = lambda p: None  # noqa: E731
    with pytest.raises(ValueError):
        bus.unsubscribe("e", cb)
    other = []
    bus.subscribe("e", other.append)
    with pytest.raises(ValueError):
        bus.unsubscribe("e", cb)  # a different callback is subscribed


def test_same_callback_on_two_events():
    bus = make_bus()
    seen = []
    bus.subscribe("a", seen.append)
    bus.subscribe("b", seen.append)
    bus.publish("a", "A")
    bus.publish("b", "B")
    assert seen == ["A", "B"]
    bus.unsubscribe("a", seen.append)
    bus.publish("a", "A2")
    bus.publish("b", "B2")
    assert seen == ["A", "B", "B2"]
