from django.contrib import admin

from hotels.models import Hotel, HotelDepartment, HotelUserRole, Role, Room


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "code"]
    search_fields = ["name"]


@admin.register(HotelDepartment)
class HotelDepartmentAdmin(admin.ModelAdmin): ...


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin): ...


@admin.register(HotelUserRole)
class HotelUserRoleAdmin(admin.ModelAdmin):
    search_fields = [
        "user__email",
        "user__username",
        "hotel__name",
        "department__name",
        "role__name",
    ]

    list_select_related = ["user", "hotel", "department", "role"]

    list_display = [
        "user",
        "hotel",
        "department",
        "role",
        "is_active",
        "created_at",
    ]
    list_filter = ["hotel", "department", "role", "is_active"]
    ordering = ["-created_at"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
