from __future__ import annotations

import uuid

from django.db import models

from common.common_base_model import BaseModel
from common.utils.formater import formater_str_models


class IssueCategory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # hotel = models.ForeignKey(
    #     "hotels.Hotel",
    #     on_delete=models.CASCADE,
    #     related_name="issue_categories",
    # )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    department = models.ForeignKey(
        "hotels.HotelDepartment",
        on_delete=models.PROTECT,
        related_name="issue_categories",
    )
    default_sla_minutes = models.PositiveIntegerField(
        blank=True, null=True
    )  # NULL => брать из department
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["name", "is_active"]),
        ]

    def __str__(self) -> str:
        return formater_str_models(self.name)


class Issue(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Status(models.TextChoices):
        NEW = "new", "New"
        ASSIGNED = "assigned", "Assigned"
        IN_PROGRESS = "in_progress", "In progress"
        WAITING_GUEST = "waiting_guest", "Waiting guest"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Source(models.TextChoices):
        GUEST_WEB = "guest_web", "Guest web"
        STAFF_APP = "staff_app", "Staff app"
        IMPORT = "import", "Import"

    hotel = models.ForeignKey(
        "hotels.Hotel", on_delete=models.CASCADE, related_name="issues"
    )

    guest_stay = models.ForeignKey(
        "users.GuestStay",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    room = models.ForeignKey(
        "hotels.Room", on_delete=models.PROTECT, related_name="issues"
    )

    category = models.ForeignKey(
        "issues.IssueCategory", on_delete=models.PROTECT, related_name="issues"
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.NEW,
        db_index=True,
    )
    priority = models.CharField(
        max_length=16, choices=Priority.choices, default=Priority.NORMAL
    )

    assigned_department = models.ForeignKey(
        "hotels.HotelDepartment",
        on_delete=models.PROTECT,
        related_name="assigned_issues",
    )
    assigned_user = models.ForeignKey(
        "users.StaffUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_issues",
    )

    sla_due_at = models.DateTimeField(db_index=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    last_guest_message_at = models.DateTimeField(blank=True, null=True)
    last_staff_response_at = models.DateTimeField(blank=True, null=True)

    source = models.CharField(
        max_length=16, choices=Source.choices, default=Source.GUEST_WEB
    )

    class Meta:
        indexes = [
            models.Index(fields=["hotel", "status"]),
            models.Index(fields=["hotel", "created_at"]),
        ]

    def __str__(self) -> str:
        return formater_str_models(self.hotel, self.status)


class IssueComment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class AuthorType(models.TextChoices):
        GUEST = "guest", "Guest"
        STAFF = "staff", "Staff"

    issue = models.ForeignKey(
        "issues.Issue", on_delete=models.CASCADE, related_name="comments"
    )

    author_type = models.CharField(max_length=16, choices=AuthorType.choices)
    author_user = models.ForeignKey(
        "users.StaffUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issue_comments",
    )

    message = models.TextField()
    is_internal = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["issue", "created_at"]),
        ]

    def __str__(self) -> str:
        return formater_str_models(self.issue, self.author_type)


class IssueAttachment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    issue = models.ForeignKey(
        "issues.Issue", on_delete=models.CASCADE, related_name="attachments"
    )
    file_url = models.URLField(max_length=1024)
    file_type = models.CharField(max_length=128)

    def __str__(self) -> str:
        return formater_str_models(self.file_url, self.file_type)


class IssueStatusHistory(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class ChangedByType(models.TextChoices):
        GUEST = "guest", "Guest"
        STAFF = "staff", "Staff"

    issue = models.ForeignKey(
        "issues.Issue", on_delete=models.CASCADE, related_name="status_history"
    )

    old_status = models.CharField(max_length=32)
    new_status = models.CharField(max_length=32)

    changed_by_type = models.CharField(
        max_length=16, choices=ChangedByType.choices
    )
    changed_by_user = models.ForeignKey(
        "users.StaffUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issue_status_changes",
    )

    class Meta:
        indexes = [
            models.Index(fields=["issue", "updated_at"]),
        ]

    def __str__(self) -> str:
        return formater_str_models(self.issue, self.changed_by_user)
