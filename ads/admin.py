from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "game_system",
        "session_frequency",
        "location_type",
        "looking_for_players",
        "looking_for_dm",
        "num_players",
        "created",
        "updated"
    )
    list_filter = (
        "game_system",
        "session_frequency",
        "location_type",
        "looking_for_players",
        "looking_for_dm",
        "created"
    )
    search_fields = (
        "title",
        "description",
        "owner__username",
        "game_system",
        "location_details"
    )
    raw_id_fields = ("owner", "table")
    autocomplete_fields = ("owner", "table")
    readonly_fields = ("created", "updated")

    fieldsets = (
        (None, {
            "fields": (
                "owner",
                "title",
                "table",
                "description",
                "game_system",
                "tags"
            )
        }),
        ("Session Info", {
            "fields": (
                "session_frequency",
                "location_type",
                "location_details"
            )
        }),
        ("Looking For", {
            "fields": (
                "looking_for_players",
                "num_players",
                "looking_for_dm"
            )
        }),
        ("Timestamps", {
            "fields": ("created", "updated")
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        ro = list(self.readonly_fields)
        if obj:
            ro += ["owner", "table"]
        return ro