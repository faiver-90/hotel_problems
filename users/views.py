from django.http import JsonResponse


def health_check(request):
    return JsonResponse(data={"result":"ok"})
