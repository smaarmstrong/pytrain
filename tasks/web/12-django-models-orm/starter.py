import django
from django.conf import settings

if not settings.configured:  # the grader configures Django before loading this
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
        USE_TZ=True,
    )
    django.setup()

    # register a stand-in app for label "solution" so reverse relations
    # (author__books) resolve in queries — the grader does the same
    from django.apps import apps
    from django.apps.config import AppConfig

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

from django.db import models  # noqa: E402


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = "solution"


class Book(models.Model):
    # title, author (FK, related_name="books"), year, pages — see prompt.md
    class Meta:
        app_label = "solution"


def add_book(author_name, title, year, pages):
    ...


def books_between(start, end):
    ...


def prolific_authors(min_books):
    ...


def average_pages(author_name):
    ...
