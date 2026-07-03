import json

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
from django.views.decorators.http import require_POST  # noqa: E402


def ping(request):
    return JsonResponse({"pong": True})


def square(request, n):
    return JsonResponse({"result": n * n})


def add(request):
    try:
        a = int(request.GET["a"])
        b = int(request.GET["b"])
    except (KeyError, ValueError):
        return JsonResponse({"error": "a and b must be integers"}, status=400)
    return JsonResponse({"sum": a + b})


@require_POST
def echo(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)
    return JsonResponse({"you_sent": body})


urlpatterns = [
    path("ping/", ping),
    path("square/<int:n>/", square),
    path("add/", add),
    path("echo/", echo),
]
