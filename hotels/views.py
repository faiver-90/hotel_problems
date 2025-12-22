from django.shortcuts import render

from hotels.models import Hotel


def list_hotels(request):
    hotels = Hotel.objects.all()

    return render(request, "hotels/list.html", {"hotels": hotels})
