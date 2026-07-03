# TypedDict user profiles

In `solution.py`, model user profiles as nested `TypedDict`s and write two
functions over them.

```python
class Address(TypedDict):
    street: str
    city: str

class UserProfile(TypedDict):
    name: str
    age: int
    address: Address          # nested TypedDict
    nickname: NotRequired[str]  # optional key


def make_profile(name: str, age: int, street: str, city: str,
                 nickname: str | None = None) -> UserProfile:
    """Build a profile dict. When nickname is None the 'nickname' KEY MUST BE
    ABSENT from the result (not present with value None)."""

def describe(profile: UserProfile) -> str:
    """'<name> (<age>) of <city>', plus ', aka <nickname>' when the
    nickname key is present."""
```

Examples:

```python
>>> make_profile("Ada", 36, "1 Duke St", "London")
{'name': 'Ada', 'age': 36, 'address': {'street': '1 Duke St', 'city': 'London'}}
>>> describe(make_profile("Ada", 36, "1 Duke St", "London", nickname="Countess"))
'Ada (36) of London, aka Countess'
```

Grading: runtime behaviour as above, plus your TypedDicts' required/optional
key sets are inspected, plus mypy must be clean on your module
(`--disallow-untyped-defs`) **and** on a snippet the grader writes that
constructs `UserProfile` values with and without `nickname` — so `nickname`
must genuinely be `NotRequired` while the other keys stay required.
