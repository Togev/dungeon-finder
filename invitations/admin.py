from django.contrib import admin
from .models import Invitation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        "ad",
        "application",
        "sender",
        "recipient",
        "status",
        "created_at",
        "responded_at",
    )
    list_filter = (
        "status",
        "created_at",
        "responded_at",
        "ad",
    )
    search_fields = (
        "ad__title",
        "sender__username",
        "recipient__username",
        "application__id",
    )
    raw_id_fields = ("ad", "application", "sender", "recipient")
    autocomplete_fields = ("ad", "application", "sender", "recipient")
    readonly_fields = ("created_at", "responded_at")

    fieldsets = (
        (None, {
            "fields": (
                "ad",
                "application",
                "sender",
                "recipient",
                "status",
            )
        }),
        ("Timestamps", {
            "fields": ("created_at", "responded_at")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        ro = list(self.readonly_fields)
        if obj:
            ro += ["ad", "application", "sender", "recipient"]
        return ro

    def has_add_permission(self, request):
        return False