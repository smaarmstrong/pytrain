import pytest

from pytrain_grader import load_solution, get_attr


def query_cls():
    return get_attr(load_solution(), "Query")


def test_minimal_query():
    Query = query_cls()
    assert Query("users").build() == "SELECT * FROM users"


def test_full_fluent_chain():
    Query = query_cls()
    sql = (Query("users")
           .select("id", "name")
           .where("age >= 18")
           .where("active = 1")
           .order_by("name", desc=True)
           .limit(10)
           .build())
    assert sql == ("SELECT id, name FROM users "
                   "WHERE age >= 18 AND active = 1 "
                   "ORDER BY name DESC LIMIT 10")


def test_select_accumulates_across_calls():
    Query = query_cls()
    sql = Query("t").select("a").select("b", "c").build()
    assert sql == "SELECT a, b, c FROM t"


def test_where_conditions_join_with_and_in_order():
    Query = query_cls()
    sql = Query("t").where("x > 1").where("y < 2").where("z = 3").build()
    assert sql == "SELECT * FROM t WHERE x > 1 AND y < 2 AND z = 3"


def test_order_by_ascending_and_descending():
    Query = query_cls()
    assert Query("t").order_by("a").build() == "SELECT * FROM t ORDER BY a"
    assert Query("t").order_by("a", desc=True).build() == "SELECT * FROM t ORDER BY a DESC"


def test_last_order_by_wins():
    Query = query_cls()
    sql = Query("t").order_by("a", desc=True).order_by("b").build()
    assert sql == "SELECT * FROM t ORDER BY b"


def test_limit_zero_is_allowed():
    Query = query_cls()
    assert Query("t").limit(0).build() == "SELECT * FROM t LIMIT 0"


def test_bad_limits_raise_valueerror():
    Query = query_cls()
    with pytest.raises(ValueError):
        Query("t").limit(-1)
    with pytest.raises(ValueError):
        Query("t").limit(2.5)
    with pytest.raises(ValueError):
        Query("t").limit("10")


def test_intermediate_variables_keep_chaining():
    Query = query_cls()
    base = Query("logs").select("ts", "msg")
    narrowed = base.where("level = 'ERROR'")
    sql = narrowed.limit(5).build()
    assert sql == "SELECT ts, msg FROM logs WHERE level = 'ERROR' LIMIT 5"


def test_build_is_repeatable():
    Query = query_cls()
    q = Query("t").select("a").where("x = 1").order_by("a").limit(3)
    first = q.build()
    second = q.build()
    assert first == second == "SELECT a FROM t WHERE x = 1 ORDER BY a LIMIT 3"
