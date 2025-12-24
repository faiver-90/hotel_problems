from django.urls import URLPattern, path

from issues.views import IssueDetailView, IssueListView, IssueStatusChangeView

urlpatterns: list[URLPattern] = [
    path("issue_list/", IssueListView.as_view(), name="issue_list"),
    path("<uuid:pk>/", IssueDetailView.as_view(), name="issue_detail"),
    path(
        "<uuid:pk>/change-status/",
        IssueStatusChangeView.as_view(),
        name="issue_change_status",
    ),
]
