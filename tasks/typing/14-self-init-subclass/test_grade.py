import typing

from pytrain_grader import load_solution, get_attr


# ---- QueryBuilder behaviour ---------------------------------------------------

def test_build_plain():
    QB = get_attr(load_solution(), "QueryBuilder")
    assert QB("users").build() == "SELECT * FROM users"


def test_build_where_and_limit():
    QB = get_attr(load_solution(), "QueryBuilder")
    q = QB("users").where("age > 21").where("active").limit(10)
    assert q.build() == "SELECT * FROM users WHERE age > 21 AND active LIMIT 10"


def test_limit_replaces():
    QB = get_attr(load_solution(), "QueryBuilder")
    assert QB("t").limit(5).limit(2).build() == "SELECT * FROM t LIMIT 2"


def test_chaining_returns_the_same_instance():
    QB = get_attr(load_solution(), "QueryBuilder")
    q = QB("t")
    assert q.where("x = 1") is q
    assert q.limit(3) is q


def test_subclass_chaining_stays_subclassed():
    QB = get_attr(load_solution(), "QueryBuilder")

    class AuditedQuery(QB):
        pass

    q = AuditedQuery("t").where("x = 1").limit(1)
    assert type(q) is AuditedQuery
    assert q.build() == "SELECT * FROM t WHERE x = 1 LIMIT 1"


# ---- Self annotations -----------------------------------------------------------

def test_chain_methods_annotated_with_self():
    QB = get_attr(load_solution(), "QueryBuilder")
    for name in ("where", "limit"):
        hints = typing.get_type_hints(getattr(QB, name))
        assert hints.get("return") is typing.Self, (
            f"{name} must be annotated to return typing.Self, "
            f"got {hints.get('return')!r}"
        )


# ---- Plugin registry ------------------------------------------------------------

def test_registers_under_lowercased_class_name():
    Plugin = get_attr(load_solution(), "Plugin")

    class CsvLoader(Plugin):
        pass

    assert Plugin.registry.get("csvloader") is CsvLoader


def test_registers_under_explicit_name_keyword():
    Plugin = get_attr(load_solution(), "Plugin")

    class JsonLoader(Plugin, name="json"):
        pass

    assert Plugin.registry.get("json") is JsonLoader
    assert "jsonloader" not in Plugin.registry


def test_init_subclass_calls_super_cooperatively():
    Plugin = get_attr(load_solution(), "Plugin")
    seen = []

    class Recording:
        def __init_subclass__(cls, **kwargs):
            seen.append(cls.__name__)
            super().__init_subclass__(**kwargs)

    class XmlLoader(Plugin, Recording, name="xml"):
        pass

    assert Plugin.registry.get("xml") is XmlLoader
    assert "XmlLoader" in seen, (
        "__init_subclass__ must call super().__init_subclass__(**kwargs) so "
        "cooperative bases still run"
    )
