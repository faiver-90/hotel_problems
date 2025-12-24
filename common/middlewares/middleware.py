from common.utils.access.scope import build_user_scope


class UserScopeMiddleware:
    """Middleware for adding user_scope to the request object."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(
            request, "user_scope"
        ):
            request._user_scope = build_user_scope(request.user)

        response = self.get_response(request)
        return response
