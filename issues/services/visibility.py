from django.db.models import QuerySet

from common.utils.access.filters import apply_scope_to_qs
from common.utils.access.scope import build_user_scope
from issues.models import Issue
from users.models import StaffUser


def _issues_base_qs() -> QuerySet[Issue]:
    return Issue.objects.select_related(
        "hotel",
        "room",
        "category",
        "assigned_department",
        "assigned_user",
    ).order_by("-created_at")


def get_visible_issues_for_user(user: StaffUser) -> QuerySet[Issue]:
    scope = build_user_scope(user)
    base_qs = _issues_base_qs()
    return apply_scope_to_qs(
        base_qs,
        scope,
        hotel_field="hotel_id",
        department_field="assigned_department_id",
    )
