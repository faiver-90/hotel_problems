from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, ListView

from issues.models import Issue

from .services.visibility import get_visible_issues_for_user


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = "issues/issue_list.html"
    context_object_name = "issues"

    def get_queryset(self):
        return get_visible_issues_for_user(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        columns = [
            "Title",
            "Room",
            "Category",
            "Status",
            "Priority",
            "Assigned",
        ]

        rows = []
        for issue in ctx["issues"]:
            rows.append(
                [
                    f"<a href='{reverse('issue_detail', args=[issue.pk])}'>{
                        issue.title
                    }</a>",
                    issue.room.number,
                    issue.category.name,
                    issue.get_status_display(),
                    issue.get_priority_display(),
                    issue.assigned_user.email if issue.assigned_user else "—",
                ]
            )

        ctx["columns"] = columns
        ctx["rows"] = rows
        return ctx


class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = "issues/issue_detail.html"
    context_object_name = "issue"
