import django
from django.conf import settings

if not settings.configured:  # the grader configures Django before loading this
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
        USE_TZ=True,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

from django.http import JsonResponse  # noqa: E402
from django.urls import path  # noqa: E402


# views: ping, square, add, echo — see prompt.md


urlpatterns = [
    # path("ping/", ...), ...
]
