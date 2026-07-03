import pytest

from shipping import quote


def test_b1_rejects_nonpositive_weight():
    with pytest.raises(ValueError):
        quote(0, "A")
    with pytest.raises(ValueError):
        quote(-3, "B")


def test_b2_rejects_unknown_zone():
    with pytest.raises(ValueError):
        quote(5, "Z")


def test_b4_light_parcel():
    assert quote(10, "B") == 13.0
    assert quote(2, "A") == 6.0


def test_b3_heavy_parcel_tiered_rate():
    assert quote(25, "B") == 19.25


def test_b5_express_multiplier():
    assert quote(10, "A", express=True) == 17.5


def test_b6_express_remote_surcharge():
    assert quote(10, "C", express=True) == 39.75


def test_b7_member_discount_small_order():
    assert quote(10, "A", member=True) == 9.0


def test_b7_member_discount_capped_at_five():
    assert quote(100, "C", express=True, member=True) == 78.5
