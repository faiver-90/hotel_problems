# issues/views.py
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView

from issues.models import Issue

from .services.status import change_issue_status
from .services.visibility import get_visible_issues_for_user


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = "issues/issue_list.html"
    context_object_name = "issues"

    def get_queryset(self):
        return get_visible_issues_for_user(self.request.user)


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = "issues/issue_detail.html"
    context_object_name = "issue"

    def get_queryset(self):
        return get_visible_issues_for_user(self.request.user)


class IssueStatusChangeView(LoginRequiredMixin, View):
    """
    Change issue status + record history + update assigned user.
    Expects a POST with the `status` field.
    """

    def post(self, request: HttpRequest, pk: str) -> HttpResponse:
        qs = get_visible_issues_for_user(request.user)
        issue = get_object_or_404(qs, pk=pk)

        new_status = request.POST.get("status")
        next_url = request.POST.get("next") or issue.get_absolute_url()

        try:
            change_issue_status(
                issue=issue, new_status=new_status, user=request.user
            )
            messages.success(request, "Status updated.")
        except ValueError as exc:
            messages.error(request, str(exc))

        return redirect(next_url)
