from django.urls import URLPattern, path

from issues.views import IssueDetailView, IssueListView

urlpatterns: list[URLPattern] = [
    path("issue_list/", IssueListView.as_view(), name="issue_list"),
    path("<uuid:pk>/", IssueDetailView.as_view(), name="issue_detail"),
]
