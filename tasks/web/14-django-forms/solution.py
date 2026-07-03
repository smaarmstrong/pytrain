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
    username = forms.CharField(min_length=3, max_length=20)
    email = forms.EmailField()
    age = forms.IntegerField(min_value=13)
    password = forms.CharField(min_length=8)
    password2 = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not username.isalnum():
            raise forms.ValidationError("letters and digits only")
        return username.lower()

    def clean(self):
        cleaned = super().clean()
        pw, pw2 = cleaned.get("password"), cleaned.get("password2")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("passwords do not match")
        return cleaned
