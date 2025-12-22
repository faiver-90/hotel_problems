from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .forms import StaffLoginForm, StaffRegisterForm
from .services.auth_tokens import AuthTokenService
from .services.jwt_cookies import JWTCookieService


class ServiceMixin:
    token_service = AuthTokenService()
    cookie_service = JWTCookieService()


class StaffLoginView(ServiceMixin, View):
    template_name = "staff/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name, {"form": StaffLoginForm()})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = StaffLoginForm(request.POST)
        if not form.is_valid():
            return render(
                request, self.template_name, {"form": form}, status=400
            )

        login_value = form.cleaned_data["username_or_email"]
        password = form.cleaned_data["password"]

        username = self.token_service.resolve_username(
            username_or_email=login_value
        )
        if not username:
            form.add_error("username_or_email", "Пользователь не найден")
            return render(
                request, self.template_name, {"form": form}, status=400
            )

        try:
            tokens = self.token_service.obtain_pair_by_username(
                username=username, password=password
            )
        except Exception:
            form.add_error(None, "Неверные учетные данные")
            return render(
                request, self.template_name, {"form": form}, status=400
            )

        resp = redirect("dashboard")
        self.cookie_service.set_tokens(
            resp, access=tokens.access, refresh=tokens.refresh
        )
        return resp


class StaffRegisterView(ServiceMixin, View):
    template_name = "staff/register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, self.template_name, {"form": StaffRegisterForm()}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = StaffRegisterForm(request.POST)
        if not form.is_valid():
            return render(
                request, self.template_name, {"form": form}, status=400
            )

        user = form.save(commit=False)
        user.is_staff = True
        user.save()

        # автологин
        tokens = self.token_service.obtain_pair_by_username(
            username=user.username,
            password=form.cleaned_data["password1"],
        )

        resp = redirect("success_register")
        self.cookie_service.set_tokens(
            resp, access=tokens.access, refresh=tokens.refresh
        )
        return resp


class SuccessRegisterView(View):
    template_name = "staff/success_register.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)


class StaffLogoutView(ServiceMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        resp = redirect("/auth/login/")
        self.cookie_service.clear(resp)
        return resp


class RefreshAccessCookieView(ServiceMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        refresh = self.cookie_service.get_refresh(request)
        if not refresh:
            return HttpResponse("No refresh token", status=401)

        try:
            access = self.token_service.refresh_access(refresh=refresh)
        except Exception:
            return HttpResponse("Invalid refresh token", status=401)

        resp = HttpResponse(status=204)
        self.cookie_service.set_access(resp, access=access)
        return resp


class Dashboard(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "users/dashboard.html")
