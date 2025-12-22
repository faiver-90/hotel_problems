from __future__ import annotations

import uuid

from django.db import models

from common.common_base_model import BaseModel


class ChannelType(models.TextChoices):
    EMAIL = "email", "Email"
    TELEGRAM = "telegram", "Telegram"
    WEB_PUSH = "web_push", "Web push"


class UserNotificationSettings(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "users.StaffUser",
        on_delete=models.CASCADE,
        related_name="notification_settings",
    )
    channel_type = models.CharField(max_length=16, choices=ChannelType.choices)
    address = models.CharField(
        max_length=255
    )  # email / telegram_chat_id / push_token
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "channel_type", "is_active"]),
        ]


class NotificationLog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(
        "users.StaffUser", on_delete=models.SET_NULL, null=True, blank=True
    )
    issue = models.ForeignKey(
        "issues.Issue", on_delete=models.SET_NULL, null=True, blank=True
    )

    channel_type = models.CharField(max_length=16, choices=ChannelType.choices)
    payload = models.JSONField()
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )

    error_message = models.TextField(blank=True, null=True)

    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "created_at"]),
        ]
