from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "ad",
        "owner",
        "recipient",
        "role",
        "status",
        "submitted_at",
        "updated_at",
    )
    list_filter = (
        "role",
        "status",
        "submitted_at",
        "ad",
    )
    search_fields = (
        "ad__title",
        "owner__username",
        "recipient__username",
        "message",
    )
    readonly_fields = ("submitted_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        ro = list(self.readonly_fields)
        if obj:
            ro += ["owner", "ad", "recipient"]
        return ro

    def has_add_permission(self, request):
        return False
