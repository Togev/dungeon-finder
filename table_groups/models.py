from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings

class Table(models.Model):
    name = models.CharField(max_length=100,
                            validators=[MinLengthValidator(3)],
                            )
    announcement = models.TextField(
        blank=True,
        help_text="Optional. This message will be shown at the top of the table for all members."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tables'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tables'
    )
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='admin_tables'
    )

    owner_color = models.CharField(
        max_length=7,
        default="#e53935"
    )

    admin_color = models.CharField(
        max_length=7,
        default="#3949ab"
    )

    member_color = models.CharField(
        max_length=7,
        default="#43a047"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name