# Django: form validation

In `solution.py`, define a Django **`forms.Form`** called `SignupForm`
that does all the input checking for a signup flow: field constraints,
a per-field `clean_<field>` hook and a cross-field `clean()` hook. No
views, no models — the grader instantiates the form directly with data
dicts and inspects `is_valid()`, `cleaned_data` and `errors`.

Keep the settings boilerplate from the starter.

## Fields

- `username` — `CharField`, min length 3, max length 20
- `email` — `EmailField`
- `age` — `IntegerField`, minimum value 13
- `password` — `CharField`, min length 8
- `password2` — `CharField` (the confirmation)

## Custom validation

1. `clean_username` — the username must contain **only letters and
   digits** (`str.isalnum()`); otherwise raise
   `ValidationError("letters and digits only")`. Return the username
   **lowercased** — `cleaned_data["username"]` for input `"AdaLovelace"`
   is `"adalovelace"`.

2. `clean()` — if both passwords are present and they differ, raise
   `ValidationError("passwords do not match")` so it lands in
   `non_field_errors()`.

Behaviour examples:

```python
form = SignupForm({"username": "Ada99", "email": "ada@example.com",
                   "age": "36", "password": "s3cret-pw", "password2": "s3cret-pw"})
form.is_valid()                      # True
form.cleaned_data["username"]        # "ada99"
form.cleaned_data["age"]             # 36 (int — forms coerce strings)

bad = SignupForm({"username": "ada lovelace", ...})
bad.is_valid()                       # False
"letters and digits only" in str(bad.errors["username"])   # True

mismatch = SignupForm({..., "password": "aaaaaaaa", "password2": "bbbbbbbb"})
mismatch.is_valid()                  # False
"passwords do not match" in mismatch.non_field_errors()    # True
```

Every field is required: an empty data dict must produce an error for
all five fields.
