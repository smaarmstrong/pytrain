import random
from collections import deque

import pytest

from pytrain_grader import load_solution, get_attr


def classes():
    mod = load_solution()
    return get_attr(mod, "Stack"), get_attr(mod, "Queue")


def test_stack_lifo_order():
    Stack, _ = classes()
    s = Stack()
    for x in [1, 2, 3]:
        s.push(x)
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]


def test_queue_fifo_order():
    _, Queue = classes()
    q = Queue()
    for x in [1, 2, 3]:
        q.enqueue(x)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


def test_peek_does_not_remove():
    Stack, Queue = classes()
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b" and len(s) == 2
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.peek() == "a" and len(q) == 2


def test_len_and_is_empty_transitions():
    Stack, Queue = classes()
    s = Stack()
    assert len(s) == 0 and s.is_empty()
    s.push(None)  # None is a valid stored value
    assert len(s) == 1 and not s.is_empty()
    assert s.pop() is None
    assert s.is_empty()

    q = Queue()
    assert q.is_empty()
    q.enqueue(None)
    assert len(q) == 1 and not q.is_empty()
    assert q.dequeue() is None
    assert q.is_empty()


def test_empty_operations_raise_indexerror():
    Stack, Queue = classes()
    s, q = Stack(), Queue()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.peek()


def test_duplicates_kept():
    Stack, Queue = classes()
    s = Stack()
    for x in [7, 7, 7]:
        s.push(x)
    assert len(s) == 3
    q = Queue()
    for x in ["x", "x"]:
        q.enqueue(x)
    assert q.dequeue() == "x" and q.dequeue() == "x"


def test_randomized_against_oracle():
    Stack, Queue = classes()
    rng = random.Random(42)
    s, q = Stack(), Queue()
    oracle_s, oracle_q = [], deque()
    for step in range(2000):
        v = rng.randrange(100)
        if rng.random() < 0.55:
            s.push(v)
            oracle_s.append(v)
            q.enqueue(v)
            oracle_q.append(v)
        else:
            if oracle_s:
                assert s.pop() == oracle_s.pop(), f"stack diverged at step {step}"
            if oracle_q:
                assert q.dequeue() == oracle_q.popleft(), f"queue diverged at step {step}"
        assert len(s) == len(oracle_s)
        assert len(q) == len(oracle_q)
        assert s.is_empty() == (not oracle_s)
        assert q.is_empty() == (not oracle_q)
