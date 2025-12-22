from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.utils import timezone
from faker import Faker
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()


@pytest.fixture()
def faker() -> Faker:
    return Faker()


@pytest.fixture()
def user_factory(faker: Faker) -> Callable[..., User]:
    def _make_user(**kwargs):
        username = kwargs.pop("username", faker.user_name()[:30])
        email = kwargs.pop("email", faker.unique.email())
        password = kwargs.pop("password", "TestPassword123!")

        user = User(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        user._raw_password = password  # type: ignore[attr-defined]
        return user

    return _make_user


@pytest.fixture()
def staff_user(user_factory) -> User:
    return user_factory(is_staff=True)


@dataclass(frozen=True)
class TokenBundle:
    access: str
    refresh: str


@pytest.fixture()
def token_bundle_for_user(staff_user: User) -> TokenBundle:
    refresh = RefreshToken.for_user(staff_user)
    access = refresh.access_token
    return TokenBundle(access=str(access), refresh=str(refresh))


@pytest.fixture()
def expired_access_for_user(staff_user: User) -> str:
    # Create an expired access token by overwriting the `exp` claim.
    token = AccessToken.for_user(staff_user)
    token["exp"] = int((timezone.now() - timedelta(seconds=30)).timestamp())
    return str(token)


@pytest.fixture()
def authed_client(client: Client, staff_user: User) -> Client:
    # session-auth: request.user будет staff_user
    client.force_login(staff_user)
    return client
