from django.contrib import admin

from issues.models import (
    Issue,
    IssueAttachment,
    IssueCategory,
    IssueComment,
    IssueStatusHistory,
)


@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "hotel", "department", "is_active"]
    list_filter = ["hotel", "department", "is_active"]
    search_fields = ["name", "description"]
    ordering = ["hotel", "name"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "hotel",
        "status",
        "priority",
        "assigned_department",
        "assigned_user",
        "created_at",
    ]
    list_filter = ["hotel", "status", "priority", "source"]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]


@admin.register(IssueComment)
class IssueCommentAdmin(admin.ModelAdmin):
    list_display = [
        "issue",
        "author_type",
        "author_user",
        "is_internal",
        "created_at",
    ]
    list_filter = ["author_type", "is_internal"]
    search_fields = ["message"]


@admin.register(IssueAttachment)
class IssueAttachmentAdmin(admin.ModelAdmin):
    list_display = ["issue", "file_type", "file_url"]
    search_fields = ["file_url"]


@admin.register(IssueStatusHistory)
class IssueStatusHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "issue",
        "old_status",
        "new_status",
        "changed_by_type",
        "changed_by_user",
        "created_at",
    ]
    list_filter = ["changed_by_type", "new_status"]
