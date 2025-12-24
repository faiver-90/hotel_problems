from __future__ import annotations

from dataclasses import dataclass

from hotels.models import HotelUserRole, Visibility
from users.models import StaffUser


@dataclass(frozen=True)
class UserScope:
    """
    General user visibility:
    - global: True → visible to all
    - hotel_ids: hotels to which access is granted
    - dept_pairs: pairs (hotel_id, department_id)
    """

    is_global: bool
    hotel_ids: frozenset[int]
    dept_pairs: frozenset[tuple[int, int]]


def build_user_scope(user: StaffUser) -> UserScope:
    roles: list[HotelUserRole] = list(
        HotelUserRole.objects.filter(user=user, is_active=True).select_related(
            "role"
        )
    )

    if not roles:
        return UserScope(
            is_global=False,
            hotel_ids=frozenset(),
            dept_pairs=frozenset(),
        )

    # GLOBAL
    if any(r.role.visibility == Visibility.GLOBAL for r in roles):
        return UserScope(
            is_global=True,
            hotel_ids=frozenset(),
            dept_pairs=frozenset(),
        )

    hotel_ids: set[int] = set()
    dept_pairs: set[tuple[int, int]] = set()

    for r in roles:
        vis = r.role.visibility

        if vis == Visibility.HOTEL and r.hotel_id is not None:
            hotel_ids.add(r.hotel_id)

        elif vis == Visibility.DEPARTMENT and r.hotel_id and r.department_id:
            dept_pairs.add((r.hotel_id, r.department_id))

    return UserScope(
        is_global=False,
        hotel_ids=frozenset(hotel_ids),
        dept_pairs=frozenset(dept_pairs),
    )
