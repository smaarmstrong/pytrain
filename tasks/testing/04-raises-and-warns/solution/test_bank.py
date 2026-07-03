import pytest

from bank import InsufficientFunds, take, withdraw


def test_withdraw_returns_new_balance():
    assert withdraw(100, 30) == 70


def test_zero_amount_rejected():
    with pytest.raises(ValueError, match="amount must be positive"):
        withdraw(100, 0)


def test_negative_amount_rejected():
    with pytest.raises(ValueError, match="amount must be positive"):
        withdraw(100, -5)


def test_overdraft_raises_insufficient_funds_with_shortfall():
    with pytest.raises(InsufficientFunds, match="short by 50"):
        withdraw(100, 150)


def test_take_warns_deprecation_and_still_works():
    with pytest.warns(DeprecationWarning, match="take is deprecated"):
        assert take(100, 30) == 70
