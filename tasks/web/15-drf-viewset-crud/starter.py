import django
from django.conf import settings

if not settings.configured:  # the grader configures Django before loading this
    settings.configure(
        DEBUG=True,
        SECRET_KEY="pytrain-test-key",
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "rest_framework",
        ],
        USE_TZ=True,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

from django.db import models  # noqa: E402
from rest_framework import routers, serializers, viewsets  # noqa: E402


class Snippet(models.Model):
    # title, code, language — see prompt.md
    class Meta:
        app_label = "solution"


class SnippetSerializer(serializers.ModelSerializer):
    ...


class SnippetViewSet(viewsets.ModelViewSet):
    ...


# router = ...
urlpatterns = []
