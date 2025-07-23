from django.db import models

from django.conf import settings


# Create your models here.
class Application(models.Model):
    ROLE_CHOICES = [
        ('dm', 'Dungeon Master'),
        ('player', 'Player'),
        ('both', 'Both'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    ad = models.ForeignKey('ads.Ad', on_delete=models.CASCADE, related_name='applications')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_applications')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_applications')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.owner} applied as {self.role} to {self.ad.title}"