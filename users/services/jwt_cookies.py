from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.conf import settings
from django.http import HttpResponse


@dataclass(frozen=True)
class JWTCookieConfig:
    access_name: str = "access_token"
    refresh_name: str = "refresh_token"
    path: str = "/"
    samesite: str = "Lax"
    httponly: bool = True

    @property
    def secure(self) -> bool:
        return False if settings.DEBUG else True

    def as_cookie_kwargs(self) -> dict[str, Any]:
        return {
            "httponly": self.httponly,
            "samesite": self.samesite,
            "secure": self.secure,
            "path": self.path,
        }


class JWTCookieService:
    """Set/clear JWT cookies in a single place."""

    def __init__(self, config: JWTCookieConfig | None = None) -> None:
        self._cfg = config or JWTCookieConfig()

    def set_tokens(
        self, resp: HttpResponse, *, access: str, refresh: str
    ) -> None:
        kwargs = self._cfg.as_cookie_kwargs()
        resp.set_cookie(self._cfg.access_name, access, **kwargs)
        resp.set_cookie(self._cfg.refresh_name, refresh, **kwargs)

    def set_access(self, resp: HttpResponse, *, access: str) -> None:
        kwargs = self._cfg.as_cookie_kwargs()
        resp.set_cookie(self._cfg.access_name, access, **kwargs)

    def clear(self, resp: HttpResponse) -> None:
        resp.delete_cookie(self._cfg.access_name, path=self._cfg.path)
        resp.delete_cookie(self._cfg.refresh_name, path=self._cfg.path)

    def get_refresh(self, request) -> str | None:
        return request.COOKIES.get(self._cfg.refresh_name)
