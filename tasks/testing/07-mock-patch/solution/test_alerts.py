from unittest.mock import call, patch

import alerts


def test_one_email_per_low_item_in_alphabetical_order():
    with patch("alerts.send_email") as sender:
        alerts.check_and_alert({"bolts": 2, "anvils": 1, "nuts": 50}, threshold=5)
    assert sender.call_args_list == [
        call("ops@example.com", "Low stock: anvils", "Only 1 left"),
        call("ops@example.com", "Low stock: bolts", "Only 2 left"),
    ]


@patch("alerts.send_email")
def test_no_email_at_or_above_threshold(sender):
    alerts.check_and_alert({"bolts": 5, "nuts": 6}, threshold=5)
    sender.assert_not_called()


@patch("alerts.send_email")
def test_empty_stock_sends_nothing(sender):
    alerts.check_and_alert({}, threshold=5)
    sender.assert_not_called()
