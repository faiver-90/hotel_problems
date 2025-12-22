from __future__ import annotations

import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

from common.common_base_model import BaseModel


def default_valid_until():
    return timezone.now() + timedelta(days=7)


class GuestStay(BaseModel):
    """
    Привязка "браузерная сессия -> отель/комната" сроком на неделю.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    hotel = models.ForeignKey(
        "hotels.Hotel", on_delete=models.CASCADE, related_name="guest_stays"
    )

    session_key = models.CharField(max_length=64, db_index=True)

    valid_until = models.DateTimeField(
        db_index=True,
        default=default_valid_until,
    )

    class Meta:
        indexes = [
            models.Index(fields=["hotel", "created_at"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["session_key"],
                name="uniq_guest_stay_session_key",
            ),
        ]


class StaffUser(AbstractUser):
    """
    Пользователи только для персонала/админов.
    Гостей как пользователей не храним.
    """

    class Language(models.TextChoices):
        EN = "en", "English"
        AR = "ar", "Arabic"
        RU = "ru", "Russian"
        OTHER = "other", "Other"

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=32, blank=True, null=True)
    language = models.CharField(
        max_length=10, choices=Language.choices, default=Language.EN
    )

    groups = models.ManyToManyField(
        Group,
        related_name="staff_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="staff_user_permissions_set",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
