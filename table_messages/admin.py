from django.contrib import admin
from .models import TableMessage

@admin.register(TableMessage)
class TableMessageAdmin(admin.ModelAdmin):
    list_display = (
        "table",
        "sender",
        "content",
        "sent_at",
    )
    list_filter = (
        "table",
        "sender",
        "sent_at",
    )
    search_fields = (
        "content",
        "sender__username",
        "table__name",
    )
    readonly_fields = ("table", "sender", "content", "sent_at")

    def has_add_permission(self, request):
        return False