"""Django ORM grader.

Django's app registry breaks if the learner's models are defined twice, so
the module is loaded ONCE and cached; each test wipes the tables instead of
reloading.
"""
import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
        USE_TZ=True,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

# Register a stand-in app config for the "solution" app label so that
# reverse relations on the learner's models resolve inside ORM queries
# (apps.get_models() only walks registered app configs).
from django.apps import apps  # noqa: E402
from django.apps.config import AppConfig  # noqa: E402

if "solution" not in apps.app_configs:
    _cfg = AppConfig.__new__(AppConfig)
    _cfg.name = _cfg.label = "solution"
    _cfg.verbose_name = "Solution"
    _cfg.module = None
    _cfg.path = ""
    _cfg.apps = apps
    _cfg.models = apps.all_models["solution"]
    apps.app_configs["solution"] = _cfg
    apps.clear_cache()

import pytest  # noqa: E402

from pytrain_grader import load_solution, get_attr  # noqa: E402

_cache = {}


def _mod():
    if "mod" not in _cache:
        mod = load_solution()
        _cache["mod"] = mod
        # build the tables for the learner's models, once
        from django.db import connection

        author = get_attr(mod, "Author")
        book = get_attr(mod, "Book")
        with connection.schema_editor() as se:
            se.create_model(author)
            se.create_model(book)
    return _cache["mod"]


@pytest.fixture()
def mod():
    m = _mod()
    get_attr(m, "Book").objects.all().delete()
    get_attr(m, "Author").objects.all().delete()
    return m


def seed(mod):
    add = get_attr(mod, "add_book")
    add("Le Guin", "A Wizard of Earthsea", 1968, 205)
    add("Le Guin", "The Dispossessed", 1974, 341)
    add("Le Guin", "The Left Hand of Darkness", 1969, 304)
    add("Herbert", "Dune", 1965, 412)
    add("Adams", "Mostly Harmless", 1992, 240)


def test_add_book_returns_saved_book(mod):
    add = get_attr(mod, "add_book")
    b = add("Le Guin", "A Wizard of Earthsea", 1968, 205)
    Book = get_attr(mod, "Book")
    assert isinstance(b, Book)
    assert b.pk is not None
    assert b.title == "A Wizard of Earthsea"
    assert b.year == 1968
    assert b.pages == 205
    assert b.author.name == "Le Guin"


def test_add_book_reuses_author(mod):
    add = get_attr(mod, "add_book")
    Author = get_attr(mod, "Author")
    add("Le Guin", "Book One", 1968, 100)
    add("Le Guin", "Book Two", 1974, 100)
    assert Author.objects.filter(name="Le Guin").count() == 1


def test_related_name_books(mod):
    add = get_attr(mod, "add_book")
    Author = get_attr(mod, "Author")
    add("Herbert", "Dune", 1965, 412)
    assert [b.title for b in Author.objects.get(name="Herbert").books.all()] == ["Dune"]


def test_books_between_inclusive_and_ordered(mod):
    seed(mod)
    f = get_attr(mod, "books_between")
    assert f(1965, 1974) == [
        "Dune",
        "A Wizard of Earthsea",
        "The Left Hand of Darkness",
        "The Dispossessed",
    ]
    # boundaries are inclusive
    assert f(1968, 1969) == ["A Wizard of Earthsea", "The Left Hand of Darkness"]


def test_books_between_ties_by_title(mod):
    add = get_attr(mod, "add_book")
    add("X", "Zebra", 2000, 10)
    add("Y", "Apple", 2000, 10)
    assert get_attr(mod, "books_between")(2000, 2000) == ["Apple", "Zebra"]


def test_books_between_empty(mod):
    seed(mod)
    assert get_attr(mod, "books_between")(1800, 1810) == []


def test_prolific_authors(mod):
    seed(mod)
    f = get_attr(mod, "prolific_authors")
    assert f(2) == ["Le Guin"]
    assert f(1) == ["Adams", "Herbert", "Le Guin"]  # ordered by name
    assert f(4) == []


def test_average_pages(mod):
    seed(mod)
    f = get_attr(mod, "average_pages")
    got = f("Le Guin")
    assert isinstance(got, float)
    assert got == pytest.approx((205 + 341 + 304) / 3)
    assert f("Herbert") == pytest.approx(412.0)


def test_average_pages_missing_author_is_none(mod):
    seed(mod)
    assert get_attr(mod, "average_pages")("Nobody") is None


def test_average_pages_author_without_books_is_none(mod):
    Author = get_attr(mod, "Author")
    Author.objects.create(name="Bookless")
    assert get_attr(mod, "average_pages")("Bookless") is None
