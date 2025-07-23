from django.db import models

from django.conf import settings
from ad_applications.models import Application
from ads.models import Ad


# Create your models here.
class Invitation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_invitations')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invitation from {self.sender} to {self.recipient} for {self.ad} (status: {self.status})"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_status = Invitation.objects.get(pk=self.pk).status
            if old_status != 'pending' and self.status != old_status:
                raise ValueError("Cannot change status once finalized.")
        super().save(*args, **kwargs)