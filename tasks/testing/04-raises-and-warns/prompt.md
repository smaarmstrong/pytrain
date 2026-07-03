# Raises, warns, and match=

Your workspace contains `bank.py`:

```python
class InsufficientFunds(Exception): ...

def withdraw(balance, amount): ...
def take(balance, amount): ...   # deprecated alias
```

Contract:

- `withdraw(balance, amount)` returns the new balance (`balance - amount`).
- `amount <= 0` raises `ValueError` with the exact message
  `"amount must be positive"` (zero counts — `withdraw(100, 0)` raises).
- `amount > balance` raises `InsufficientFunds` with the exact message
  `f"short by {amount - balance}"` — e.g. `withdraw(100, 150)` raises
  `InsufficientFunds("short by 50")`.
- `take(balance, amount)` behaves exactly like `withdraw`, but first emits a
  `DeprecationWarning` with the message `"take is deprecated; use withdraw"`.

## Your job

Write `test_bank.py`. The exception **types**, their **messages**, and the
warning's **category and message** are all part of the contract — pin them
down with `pytest.raises(..., match=...)` and `pytest.warns(..., match=...)`.
Cover the happy path too.

## How it is graded

Your `test_bank.py` is copied — alone — next to one correct and several buggy
implementations of `bank.py` (wrong exception type, wrong message, wrong
shortfall number, missing/wrong-category warning, boundary bug, wrong
balance). It must pass the correct one and fail every buggy one. Keep
everything in `test_bank.py`; develop against the correct `bank.py` in your
workspace with `python -m pytest -q`.
