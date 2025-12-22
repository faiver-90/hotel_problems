from __future__ import annotations

import pytest
from django.http import HttpRequest, HttpResponse
from django.test import RequestFactory
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from users.middleware import JWTRefreshMiddleware


def _get_response_ok(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("OK", status=200)


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_middleware_no_access_cookie_passthrough(rf: RequestFactory):
    req = rf.get("/dashboard/")
    req.COOKIES = {}  # type: ignore[attr-defined]

    mw = JWTRefreshMiddleware(_get_response_ok)
    resp = mw(req)
    assert resp.status_code == 200
    assert resp.content == b"OK"


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_middleware_valid_access_passthrough(
    rf: RequestFactory, token_bundle_for_user
):
    req = rf.get("/dashboard/")
    req.COOKIES = {"access_token": token_bundle_for_user.access}  # type: ignore[attr-defined]

    mw = JWTRefreshMiddleware(_get_response_ok)
    resp = mw(req)
    assert resp.status_code == 200
    assert "access_token" not in resp.cookies  # не должен перезаписывать


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_middleware_expired_access_and_valid_refresh_sets_new_access(
    rf: RequestFactory,
    expired_access_for_user: str,
    staff_user,
):
    refresh = RefreshToken.for_user(staff_user)

    req = rf.get("/dashboard/")
    req.COOKIES = {
        "access_token": expired_access_for_user,
        "refresh_token": str(refresh),
    }  # type: ignore[attr-defined]

    mw = JWTRefreshMiddleware(_get_response_ok)
    resp = mw(req)

    assert resp.status_code == 200
    assert "access_token" in resp.cookies  # должен выставить новый access


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_middleware_expired_access_no_refresh_redirects_and_clears(
    rf: RequestFactory,
    expired_access_for_user: str,
):
    req = rf.get("/dashboard/")
    req.COOKIES = {"access_token": expired_access_for_user}  # type: ignore[attr-defined]

    mw = JWTRefreshMiddleware(_get_response_ok)
    resp = mw(req)

    assert resp.status_code == 302
    assert resp.url.endswith(reverse("staff_login"))
    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies


@override_settings(ROOT_URLCONF="users.urls")
@pytest.mark.django_db
def test_middleware_expired_access_invalid_refresh_redirects_and_clears(
    rf: RequestFactory,
    expired_access_for_user: str,
):
    req = rf.get("/dashboard/")
    req.COOKIES = {
        "access_token": expired_access_for_user,
        "refresh_token": "invalid",
    }  # type: ignore[attr-defined]

    mw = JWTRefreshMiddleware(_get_response_ok)
    resp = mw(req)

    assert resp.status_code == 302
    assert resp.url.endswith(reverse("staff_login"))
    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies
