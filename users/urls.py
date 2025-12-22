from django.urls import path

from users.views import health_check

urlpatterns = [
    path("health_check/", health_check, name="health_check"),
]
