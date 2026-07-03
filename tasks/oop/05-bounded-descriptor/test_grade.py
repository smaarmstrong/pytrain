import pytest

from pytrain_grader import load_solution, get_attr


def bounded_cls():
    return get_attr(load_solution(), "Bounded")


def make_player(Bounded):
    class Player:
        health = Bounded(0, 100)
        mana = Bounded(0, 50)

        def __init__(self, health, mana):
            self.health = health
            self.mana = mana

    return Player


def test_valid_values_round_trip():
    Player = make_player(bounded_cls())
    p = Player(80, 20)
    assert p.health == 80
    assert p.mana == 20


def test_bounds_are_inclusive():
    Player = make_player(bounded_cls())
    p = Player(0, 50)
    assert p.health == 0
    assert p.mana == 50
    p.health = 100
    assert p.health == 100


def test_out_of_range_raises_valueerror():
    Player = make_player(bounded_cls())
    p = Player(80, 20)
    with pytest.raises(ValueError):
        p.health = 101
    with pytest.raises(ValueError):
        p.mana = -1


def test_validation_applies_inside_init_too():
    Player = make_player(bounded_cls())
    with pytest.raises(ValueError):
        Player(150, 20)


def test_non_number_raises_typeerror():
    Player = make_player(bounded_cls())
    p = Player(80, 20)
    with pytest.raises(TypeError):
        p.health = "full"
    with pytest.raises(TypeError):
        p.mana = [10]


def test_failed_assignment_keeps_previous_value():
    Player = make_player(bounded_cls())
    p = Player(80, 20)
    with pytest.raises(ValueError):
        p.health = 999
    with pytest.raises(TypeError):
        p.health = None
    assert p.health == 80


def test_instances_are_independent():
    Player = make_player(bounded_cls())
    a = Player(10, 5)
    b = Player(90, 40)
    a.health = 33
    assert a.health == 33
    assert b.health == 90


def test_two_descriptors_on_one_class_are_independent():
    Player = make_player(bounded_cls())
    p = Player(80, 20)
    p.mana = 7
    assert p.health == 80
    assert p.mana == 7


def test_read_before_assignment_raises_attributeerror():
    Bounded = bounded_cls()

    class Gauge:
        level = Bounded(1, 10)

    g = Gauge()
    with pytest.raises(AttributeError):
        g.level
    g.level = 5
    assert g.level == 5


def test_class_access_returns_the_descriptor_object():
    Bounded = bounded_cls()
    d = Bounded(0, 100)
    Owner = type("Owner", (), {"score": d})
    assert Owner.score is d


def test_reusable_across_owner_classes_with_different_bounds():
    Bounded = bounded_cls()

    class Freezer:
        temp = Bounded(-30, 0)

    class Oven:
        temp = Bounded(50, 250)

    f, o = Freezer(), Oven()
    f.temp = -18
    o.temp = 180
    assert f.temp == -18
    assert o.temp == 180
    with pytest.raises(ValueError):
        f.temp = 180
    with pytest.raises(ValueError):
        o.temp = -18
