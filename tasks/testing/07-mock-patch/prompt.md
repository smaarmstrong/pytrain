# Mock the mailer

Your workspace contains `alerts.py`:

```python
def send_email(to, subject, body): ...   # ALWAYS raises RuntimeError here
def check_and_alert(stock, threshold): ...
```

- `send_email` is a stand-in for a real mail transport: outside production it
  **always raises** `RuntimeError`. You cannot call it for real in a test —
  you must patch it (`unittest.mock.patch("alerts.send_email")`), as a
  decorator or a context manager.
- `check_and_alert(stock, threshold)` — `stock` is a `dict` of item name to
  quantity. For **each** item whose quantity is **strictly below**
  `threshold`, in **alphabetical order** of name, it calls:

  ```python
  send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")
  ```

  Items at or above the threshold get no email. It returns `None` — the
  **only observable effect is the calls made to `send_email`**.

## Your job

Write `test_alerts.py`. Patch `alerts.send_email` with a `Mock` and assert on
what was (and wasn't) called: how many times, with which arguments, in which
order (`mock.call_args_list`, `mock.assert_not_called`, `unittest.mock.call`
are your tools). Use `patch` at least once as a decorator and once as a
context manager if you want the full workout — both forms work.

## How it is graded

Your `test_alerts.py` is copied — alone — next to one correct and several
buggy implementations of `alerts.py` (`<=` instead of `<`, wrong recipient,
subject without the item name, only the first low item alerted, one batch
email instead of one per item). All of them return `None` — **only call
assertions can tell them apart**. Your suite must pass the correct one and
fail every buggy one. Develop with `python -m pytest -q`.
