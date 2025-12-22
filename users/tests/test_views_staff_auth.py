from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse

User = get_user_model()


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_login_get_ok(client: Client):
    resp = client.get(reverse("staff_login"))
    assert resp.status_code == 200


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_login_post_invalid_form_returns_400(client: Client):
    resp = client.post(reverse("staff_login"), data={"username_or_email": ""})
    assert resp.status_code == 400


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_login_post_unknown_user_returns_400(client: Client):
    resp = client.post(
        reverse("staff_login"),
        data={"username_or_email": "unknown@example.com", "password": "x"},
    )
    assert resp.status_code == 400
    # ошибка добавляется в поле username_or_email
    # :contentReference[oaicite:6]{index=6}


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_login_post_ok_sets_session_and_cookies(
    client: Client, staff_user: User
):
    resp = client.post(
        reverse("staff_login"),
        data={
            "username_or_email": staff_user.email,
            "password": staff_user._raw_password,  # type: ignore[attr-defined]
        },
    )
    assert resp.status_code == 302
    assert resp.url.endswith(reverse("dashboard"))

    # session-auth должен появиться
    resp2 = client.get(reverse("dashboard"))
    assert resp2.status_code == 200

    # cookies должны быть выставлены :contentReference[oaicite:7]{index=7}
    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_login_wrong_password_returns_400(client: Client, staff_user: User):
    resp = client.post(
        reverse("staff_login"),
        data={
            "username_or_email": staff_user.username,
            "password": "wrong-pass",
        },
    )
    assert resp.status_code == 400


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_register_get_ok(client: Client):
    resp = client.get(reverse("staff_register"))
    assert resp.status_code == 200


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_register_post_ok_creates_staff_and_sets_cookies(
    client: Client, faker
):
    username = faker.user_name()[:30]
    email = faker.unique.email()
    password = "TestPassword123!"

    resp = client.post(
        reverse("staff_register"),
        data={
            "username": username,
            "email": email,
            "password1": password,
            "password2": password,
            # language optional
        },
    )
    assert resp.status_code == 302
    assert resp.url.endswith(reverse("success_register"))

    u = User.objects.get(username=username)
    assert (
        u.is_staff is True
    )  # выставляется в view :contentReference[oaicite:8]{index=8}

    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_dashboard_requires_login(client: Client):
    resp = client.get(reverse("dashboard"))
    assert resp.status_code == 302
    assert reverse("staff_login") in resp.url


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_logout_post_clears_cookies_and_logs_out(authed_client: Client):
    resp = authed_client.post(reverse("staff_logout"))
    assert resp.status_code == 302
    assert resp.url.endswith(reverse("staff_login"))
    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_refresh_access_cookie_no_refresh_returns_401(client: Client):
    resp = client.post(reverse("staff_refresh_access"))
    assert resp.status_code == 401


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_refresh_access_cookie_ok_sets_access_cookie(
    client: Client, token_bundle_for_user
):
    client.cookies["refresh_token"] = token_bundle_for_user.refresh
    resp = client.post(reverse("staff_refresh_access"))
    assert resp.status_code == 204
    assert "access_token" in resp.cookies


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_refresh_access_cookie_invalid_refresh_returns_401(client: Client):
    client.cookies["refresh_token"] = "invalid"
    resp = client.post(reverse("staff_refresh_access"))
    assert resp.status_code == 401
