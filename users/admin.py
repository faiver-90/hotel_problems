from django.contrib import admin

from users.models import GuestStay, StaffUser


@admin.register(GuestStay)
class GuestStayAdmin(admin.ModelAdmin): ...


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin): ...
