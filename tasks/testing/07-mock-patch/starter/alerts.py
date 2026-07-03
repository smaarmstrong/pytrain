"""A correct implementation of the spec in prompt.md — write tests for it."""


def send_email(to, subject, body):
    """Pretend mail transport — never callable outside production."""
    raise RuntimeError("email transport is disabled outside production — patch me")


def check_and_alert(stock, threshold):
    for name in sorted(stock):
        qty = stock[name]
        if qty < threshold:
            send_email("ops@example.com", f"Low stock: {name}", f"Only {qty} left")
