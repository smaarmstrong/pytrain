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
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.CharField(max_length=30, default="python")

    class Meta:
        app_label = "solution"


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "language"]


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all().order_by("id")
    serializer_class = SnippetSerializer


router = routers.DefaultRouter()
router.register("snippets", SnippetViewSet)

urlpatterns = router.urls
