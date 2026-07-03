from typing import NotRequired, TypedDict


class Address(TypedDict):
    street: str
    city: str


class UserProfile(TypedDict):
    name: str
    age: int
    address: Address
    nickname: NotRequired[str]


def make_profile(name: str, age: int, street: str, city: str,
                 nickname: str | None = None) -> UserProfile:
    profile: UserProfile = {
        "name": name,
        "age": age,
        "address": {"street": street, "city": city},
    }
    if nickname is not None:
        profile["nickname"] = nickname
    return profile


def describe(profile: UserProfile) -> str:
    text = f"{profile['name']} ({profile['age']}) of {profile['address']['city']}"
    if "nickname" in profile:
        text += f", aka {profile['nickname']}"
    return text
