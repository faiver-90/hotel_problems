def layout_context(request):
    return {
        "current_user": request.user,
        "site_name": "===========Hotels Platform===========",
    }
