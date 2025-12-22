from __future__ import annotations

from dataclasses import dataclass

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

User = get_user_model()


@dataclass(frozen=True)
class TokenPair:
    access: str
    refresh: str


class AuthTokenService:
    """Work with SimpleJWT serializers (obtain/refresh) in one place."""

    def obtain_pair_by_username(
        self, *, username: str, password: str
    ) -> TokenPair:
        serializer = TokenObtainPairSerializer(
            data={"username": username, "password": password}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return TokenPair(access=data["access"], refresh=data["refresh"])

    def refresh_access(self, *, refresh: str) -> str:
        serializer = TokenRefreshSerializer(data={"refresh": refresh})
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data["access"]

    def resolve_username(self, *, username_or_email: str) -> str | None:
        """Если это email — вернуть username. Иначе вернуть как есть."""
        value = username_or_email.strip()
        if "@" not in value:
            return value

        user = (
            User.objects.filter(email__iexact=value).only("username").first()
        )
        return user.username if user else None
