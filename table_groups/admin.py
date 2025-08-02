from django.contrib import admin

from .forms import TableAdminForm
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm
    list_display = (
        "name",
        "created_by",
        "created_at",
        "get_member_count",
        "get_admin_count",
    )
    list_filter = ("created_by", "created_at")
    search_fields = ("name", "created_by__username")
    raw_id_fields = ("created_by",)
    autocomplete_fields = ("created_by",)
    filter_horizontal = ("members", "admins")
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": (
                "name",
                "announcement",
                "created_by",
                "members",
                "admins",
            )
        }),
        ("Colors", {
            "fields": (
                "owner_color",
                "admin_color",
                "member_color"
            )
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = "Member Count"

    def get_admin_count(self, obj):
        return obj.admins.count()
    get_admin_count.short_description = "Admin Count"