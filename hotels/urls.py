from django.urls import URLPattern, path

from hotels.views import list_hotels

urlpatterns: list[URLPattern] = [
    path("list_hotels/", list_hotels, name="list_hotels"),
]
