def divide(a, b):
    """a divided by b: divide(10, 2) -> 5.0. Let b == 0 raise naturally."""
    return a / b


def test_divide():
    """assert divide's answers; assert divide(1, 0) raises ZeroDivisionError."""
    assert divide(10, 2) == 5.0
    assert divide(1, 4) == 0.25
    try:
        divide(1, 0)
        assert False, "expected ZeroDivisionError"
    except ZeroDivisionError:
        pass
