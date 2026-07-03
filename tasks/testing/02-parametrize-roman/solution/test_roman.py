import pytest

from roman import to_roman

CASES = [
    pytest.param(1, "I", id="one", marks=pytest.mark.boundary),
    pytest.param(4, "IV", id="four"),
    pytest.param(9, "IX", id="nine"),
    pytest.param(40, "XL", id="forty"),
    pytest.param(90, "XC", id="ninety"),
    pytest.param(1994, "MCMXCIV", id="mcmxciv"),
    pytest.param(3999, "MMMCMXCIX", id="max", marks=pytest.mark.boundary),
]


@pytest.mark.parametrize("n,expected", CASES)
def test_to_roman(n, expected):
    assert to_roman(n) == expected


@pytest.mark.parametrize("bad", [0, -1, 4000])
def test_out_of_range_raises(bad):
    with pytest.raises(ValueError):
        to_roman(bad)
