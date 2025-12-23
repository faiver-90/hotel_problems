from django.contrib import admin

from hotels.models import Hotel, HotelDepartment, HotelUserRole, Role, Room


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "code"]
    search_fields = ["name"]


@admin.register(HotelDepartment)
class HotelDepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


@admin.register(HotelUserRole)
class HotelUserRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
