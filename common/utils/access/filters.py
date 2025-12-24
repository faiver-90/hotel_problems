from __future__ import annotations

from django.db.models import Q, QuerySet

from .scope import UserScope


def apply_scope_to_qs(
    qs: QuerySet,
    scope: UserScope,
    *,
    hotel_field: str = "hotel_id",
    department_field: str | None = None,
) -> QuerySet:
    """
    Applies a scope to an arbitrary QuerySet.

    - If scope.is_global → returns the original qs (everything is visible).
    - Otherwise, it assembles a Q from the list of hotels and (optionally)
    (hotel, department) pairs..
    """
    if scope.is_global:
        return qs

    if not scope.hotel_ids and not scope.dept_pairs:
        return qs.none()

    visibility_filter = Q()

    if scope.hotel_ids:
        visibility_filter |= Q(**{f"{hotel_field}__in": scope.hotel_ids})

    if department_field is not None and scope.dept_pairs:
        for hotel_id, department_id in scope.dept_pairs:
            visibility_filter |= Q(
                **{
                    hotel_field: hotel_id,
                    department_field: department_id,
                }
            )

    if not visibility_filter:
        return qs.none()

    return qs.filter(visibility_filter).distinct()
