# issues/services/status.py
from __future__ import annotations

from django.utils import timezone

from issues.models import Issue, IssueStatusHistory
from users.models import StaffUser


def change_issue_status(
    *, issue: Issue, new_status: str, user: StaffUser
) -> None:
    """
    Change the Issue status, record the history, and update the assigned user.
    """
    old_status = issue.status

    if new_status not in Issue.Status.values:
        raise ValueError(f"Unknown status: {new_status}")

    if new_status == old_status and issue.assigned_user_id == user.id:
        return

    IssueStatusHistory.objects.create(
        issue=issue,
        old_status=old_status,
        new_status=new_status,
        changed_by_type=IssueStatusHistory.ChangedByType.STAFF,
        changed_by_user=user,
    )

    issue.status = new_status
    issue.assigned_user = user

    now = timezone.now()

    if new_status == Issue.Status.RESOLVED:
        issue.resolved_at = now
    if new_status == Issue.Status.CLOSED:
        issue.closed_at = now
    issue.save(
        update_fields=[
            "status",
            "assigned_user",
            "resolved_at",
            "closed_at",
            "updated_at",
        ]
    )
