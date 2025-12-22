from __future__ import annotations

from django.http import HttpRequest, HttpResponse

from users.services.jwt_cookies import JWTCookieConfig, JWTCookieService


def test_cookie_config_secure_depends_on_debug(settings):
    settings.DEBUG = True
    cfg = JWTCookieConfig()
    assert cfg.secure is False

    settings.DEBUG = False
    cfg = JWTCookieConfig()
    assert cfg.secure is True


def test_set_tokens_and_get_refresh(settings):
    settings.DEBUG = True
    svc = JWTCookieService()

    resp = HttpResponse()
    svc.set_tokens(resp, access="a1", refresh="r1")

    # Django кладет set-cookie в headers, проверяем по cookies
    assert resp.cookies["access_token"].value == "a1"
    assert resp.cookies["refresh_token"].value == "r1"

    req = HttpRequest()
    req.COOKIES = {"refresh_token": "r1"}  # type: ignore[attr-defined]
    assert svc.get_refresh(req) == "r1"


def test_set_access(settings):
    settings.DEBUG = True
    svc = JWTCookieService()

    resp = HttpResponse()
    svc.set_access(resp, access="new_access")
    assert resp.cookies["access_token"].value == "new_access"


def test_clear_sets_deletions():
    cfg = JWTCookieConfig(path="/")
    svc = JWTCookieService(cfg)

    resp = HttpResponse()
    svc.clear(resp)

    # delete_cookie writes Set-Cookie with expires/max-age,
    # we only assert keys exist

    assert "access_token" in resp.cookies
    assert "refresh_token" in resp.cookies
