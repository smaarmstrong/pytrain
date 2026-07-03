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

from django import forms  # noqa: E402


class SignupForm(forms.Form):
    # username, email, age, password, password2 — see prompt.md
    ...

    # def clean_username(self): ...
    # def clean(self): ...
