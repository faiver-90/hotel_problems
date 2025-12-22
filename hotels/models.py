from __future__ import annotations

import uuid

from django.db import models

from common.common_base_model import BaseModel


class Hotel(BaseModel):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField(primary_key=True, editable=False)

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=32, unique=True, db_index=True)  # из QR
    timezone = models.CharField(max_length=64, default="Africa/Cairo")
    address = models.CharField(max_length=512, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self) -> str:
        return f"{self.code} — {self.name}"


class HotelDepartment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16)  # HK / ENG / REC ...
    default_sla_minutes = models.PositiveIntegerField(default=60)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("hotel", "code")]
        indexes = [
            models.Index(fields=["hotel", "code"]),
        ]

    def __str__(self) -> str:
        return f"{self.hotel.code}:{self.code}"


class Role(BaseModel):
    """
    Роли только для персонала.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(
        max_length=32, unique=True
    )  # staff/dept_manager/ops_manager/gm/admin
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.code


class HotelUserRole(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "users.StaffUser", on_delete=models.CASCADE, related_name="hotel_roles"
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="user_roles"
    )
    department = models.ForeignKey(
        HotelDepartment,
        on_delete=models.SET_NULL,
        related_name="user_roles",
        blank=True,
        null=True,
    )
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, related_name="user_roles"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["hotel", "user"]),
            models.Index(fields=["hotel", "department"]),
        ]


class Room(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name="rooms"
    )
    number = models.CharField(max_length=32)  # 101A
    building = models.CharField(max_length=64, blank=True, null=True)
    floor = models.CharField(max_length=16, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "number"], name="uniq_room_hotel_number"
            ),
        ]
        indexes = [
            models.Index(fields=["hotel", "number"]),
        ]

    def __str__(self) -> str:
        return f"{self.hotel.code}:{self.number}"
