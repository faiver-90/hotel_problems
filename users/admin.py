from django.contrib import admin

from users.models import GuestStay, StaffUser


class GuestStayAdmin(admin.ModelAdmin): ...


class StaffUserAdmin(admin.ModelAdmin): ...


admin.site.register(GuestStay, GuestStayAdmin)
admin.site.register(StaffUser, StaffUserAdmin)
