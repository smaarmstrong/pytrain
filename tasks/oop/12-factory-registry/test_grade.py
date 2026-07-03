import pytest

from pytrain_grader import load_solution, get_attr


class CsvExporter:
    def __init__(self, path, delimiter=","):
        self.path = path
        self.delimiter = delimiter


class JsonExporter:
    def __init__(self, indent=2):
        self.indent = indent


def api():
    mod = load_solution()  # fresh module (and fresh registry) per test
    return (get_attr(mod, "register"), get_attr(mod, "create"),
            get_attr(mod, "registered_names"))


def test_registry_starts_empty():
    register, create, registered_names = api()
    assert registered_names() == []
    with pytest.raises(ValueError):
        create("anything")


def test_registered_class_is_constructible_by_name():
    register, create, registered_names = api()
    register("csv")(CsvExporter)
    obj = create("csv", "out.csv", delimiter=";")
    assert isinstance(obj, CsvExporter)
    assert obj.path == "out.csv"
    assert obj.delimiter == ";"


def test_decorator_returns_the_class_unchanged():
    register, create, registered_names = api()
    result = register("csv")(CsvExporter)
    assert result is CsvExporter


def test_multiple_registrations_and_sorted_names():
    register, create, registered_names = api()
    register("json")(JsonExporter)
    register("csv")(CsvExporter)
    assert registered_names() == ["csv", "json"]
    assert isinstance(create("json"), JsonExporter)
    assert isinstance(create("csv", "a.csv"), CsvExporter)


def test_unknown_name_raises_valueerror():
    register, create, registered_names = api()
    register("csv")(CsvExporter)
    with pytest.raises(ValueError):
        create("xml")


def test_duplicate_name_raises_and_original_survives():
    register, create, registered_names = api()
    register("export")(CsvExporter)
    with pytest.raises(ValueError):
        register("export")(JsonExporter)
    assert isinstance(create("export", "p.csv"), CsvExporter)
    assert registered_names() == ["export"]


def test_kwargs_defaults_flow_through():
    register, create, registered_names = api()
    register("json")(JsonExporter)
    assert create("json").indent == 2
    assert create("json", indent=4).indent == 4
