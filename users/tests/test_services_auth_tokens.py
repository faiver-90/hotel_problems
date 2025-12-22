from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from users.services.auth_tokens import AuthTokenService

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "value,is_email,exists,expected_is_none",
    [
        ("plain_username", False, False, False),
        ("some@email.com", True, False, True),
        ("some@email.com", True, True, False),
        ("  some@email.com  ", True, True, False),
    ],
)
def test_resolve_username(
    value, is_email, exists, expected_is_none, user_factory, faker
):
    if is_email and exists:
        u = user_factory(email=value.strip(), username="the_user")
        assert u.username == "the_user"

    username = AuthTokenService.resolve_username(username_or_email=value)
    assert (username is None) == expected_is_none
    if username is not None and "@" not in value:
        assert username == value


@pytest.mark.django_db
def test_obtain_pair_by_username_ok(staff_user):
    tokens = AuthTokenService.obtain_pair_by_username(
        username=staff_user.username,
        password=staff_user._raw_password,  # type: ignore[attr-defined]
    )
    assert isinstance(tokens.access, str) and tokens.access
    assert isinstance(tokens.refresh, str) and tokens.refresh
    assert tokens.access != tokens.refresh


@pytest.mark.django_db
def test_obtain_pair_by_username_wrong_password_raises(staff_user):
    with pytest.raises(ValidationError):
        AuthTokenService.obtain_pair_by_username(
            username=staff_user.username,
            password="wrong-password",
        )


@pytest.mark.django_db
def test_refresh_access_ok(token_bundle_for_user):
    new_access = AuthTokenService.refresh_access(
        refresh=token_bundle_for_user.refresh
    )
    assert isinstance(new_access, str) and new_access
    assert new_access != token_bundle_for_user.access


@pytest.mark.django_db
def test_refresh_access_invalid_refresh_raises():
    with pytest.raises(ValidationError):
        AuthTokenService.refresh_access(refresh="not-a-real-refresh-token")
