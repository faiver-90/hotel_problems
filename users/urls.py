from django.urls import URLPattern, path

from .views import (
    Dashboard,
    RefreshAccessCookieView,
    StaffLoginView,
    StaffLogoutView,
    StaffRegisterView,
    SuccessRegisterView,
)

urlpatterns: list[URLPattern] = [
    path("login/", StaffLoginView.as_view(), name="staff_login"),
    path("register/", StaffRegisterView.as_view(), name="staff_register"),
    path("logout/", StaffLogoutView.as_view(), name="staff_logout"),
    path(
        "refresh/",
        RefreshAccessCookieView.as_view(),
        name="staff_refresh_access",
    ),
    path(
        "success_register/",
        SuccessRegisterView.as_view(),
        name="success_register",
    ),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
]
