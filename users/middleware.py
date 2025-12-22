from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

from users.services.auth_tokens import AuthTokenService
from users.services.jwt_cookies import JWTCookieService


class JWTRefreshMiddleware:
    """
    Минимальный auto-refresh:
    - работает только если есть access_token cookie
    - обновляет access, если он истёк и есть refresh
    - без редиректов на refresh endpoint (чтобы не было циклов и 405)
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.tokens = AuthTokenService()
        self.cookies = JWTCookieService()

    def __call__(self, request: HttpRequest) -> HttpResponse:
        access = request.COOKIES.get("access_token")
        if not access:
            return self.get_response(request)

        try:
            AccessToken(access)
            return self.get_response(request)
        except (InvalidToken, TokenError):
            pass

        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            resp = redirect(reverse("staff_login"))
            self.cookies.clear(resp)
            return resp

        try:
            new_access = self.tokens.refresh_access(refresh=refresh)
        except Exception:
            resp = redirect(reverse("staff_login"))
            self.cookies.clear(resp)
            return resp

        response = self.get_response(request)
        self.cookies.set_access(response, access=new_access)
        return response
