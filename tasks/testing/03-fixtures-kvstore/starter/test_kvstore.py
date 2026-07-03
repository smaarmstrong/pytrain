"""Write your fixture-based tests for kvstore here.

Run them locally with:  python -m pytest -q
"""
import pytest

import kvstore


@pytest.fixture
def store():
    # TODO: connect, yield the store, and guarantee it is closed afterwards.
    ...


def test_replace_me(store):
    # TODO: replace with focused tests covering the whole contract.
    assert False, "write your tests"
