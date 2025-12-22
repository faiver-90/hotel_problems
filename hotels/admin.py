from django.contrib import admin

from hotels.models import Hotel, HotelDepartment, HotelUserRole, Role


class HotelAdmin(admin.ModelAdmin):
    ordering = ["name"]
    list_display = ["name", "code"]
    search_fields = ["name"]


class HotelDepartmentAdmin(admin.ModelAdmin):
    pass


class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "code"]


class HotelUserRoleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelDepartment, HotelDepartmentAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(HotelUserRole, HotelUserRoleAdmin)
