from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from hotels.models import HotelUserRole, Visibility
from issues.models import Issue

if TYPE_CHECKING:
    from users.models import StaffUser


def _issues_base_qs() -> QuerySet[Issue]:
    """
    A basic queryset for Issue with the required select_related and sorting.
    """
    return Issue.objects.select_related(
        "hotel",
        "room",
        "category",
        "assigned_department",
        "assigned_user",
    ).order_by("-created_at")


def get_visible_issues_for_user(user: StaffUser) -> QuerySet[Issue]:
    """
    Return the queryset of Issues that the user has permission to see.

    The logic is based on HotelUserRole + Role.visibility:

    - Visibility.GLOBAL → all Issues across all hotels.
    - Visibility.HOTEL → all Issues for the user's specific hotels.
    - Visibility.DEPARTMENT → Issues only for their departments in their
    hotels.
    """
    # Один запрос к ролям
    roles = list(
        HotelUserRole.objects.filter(user=user, is_active=True).select_related(
            "hotel", "department", "role"
        )
    )

    if not roles:
        return Issue.objects.none()

    # 1) GLOBAL → Admin, sees all issues for all hotels
    if any(r.role.visibility == Visibility.GLOBAL for r in roles):
        return _issues_base_qs()

    # 2) Считаем права по HOTEL и DEPARTMENT в памяти
    hotel_ids: set[int] = set()
    dept_pairs: set[tuple[int, int]] = set()

    for r in roles:
        vis = r.role.visibility

        if vis == Visibility.HOTEL and r.hotel_id is not None:
            hotel_ids.add(r.hotel_id)

        elif (
            vis == Visibility.DEPARTMENT
            and r.hotel_id is not None
            and r.department_id is not None
        ):
            # It is important to maintain the connection (hotel, department)
            dept_pairs.add((r.hotel_id, r.department_id))

    # 3) Assembling a Q-filter
    visibility_filter = Q()

    if hotel_ids:
        visibility_filter |= Q(hotel_id__in=hotel_ids)

    for hotel_id, department_id in dept_pairs:
        visibility_filter |= Q(
            hotel_id=hotel_id, assigned_department_id=department_id
        )

    if not visibility_filter:
        return Issue.objects.none()

    # 4) One request to Issue
    return _issues_base_qs().filter(visibility_filter).distinct()
