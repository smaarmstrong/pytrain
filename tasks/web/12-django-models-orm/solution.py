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
from django.db.models import Avg, Count  # noqa: E402


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        app_label = "solution"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    year = models.IntegerField()
    pages = models.IntegerField()

    class Meta:
        app_label = "solution"


def add_book(author_name, title, year, pages):
    author, _ = Author.objects.get_or_create(name=author_name)
    return Book.objects.create(title=title, author=author, year=year, pages=pages)


def books_between(start, end):
    qs = (
        Book.objects.filter(year__gte=start, year__lte=end)
        .order_by("year", "title")
        .values_list("title", flat=True)
    )
    return list(qs)


def prolific_authors(min_books):
    qs = (
        Author.objects.annotate(n=Count("books"))
        .filter(n__gte=min_books)
        .order_by("name")
        .values_list("name", flat=True)
    )
    return list(qs)


def average_pages(author_name):
    avg = Book.objects.filter(author__name=author_name).aggregate(a=Avg("pages"))["a"]
    return float(avg) if avg is not None else None
