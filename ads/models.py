from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

class Ad(models.Model):
    LOCATION_CHOICES = [
        ('Online', 'Online'),
        ('In Person', 'In Person'),
        # add more as needed
    ]
    SESSION_FREQUENCY_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Biweekly', 'Biweekly'),
        ('Monthly', 'Monthly'),
        ('One-shot', 'One-shot'),
        ('Infrequent', 'Infrequent'),
        # add more as needed
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    looking_for_players = models.BooleanField(default=False)
    looking_for_dm = models.BooleanField(default=False)
    num_players = models.PositiveSmallIntegerField(null=True, blank=True)
    game_system = models.CharField(max_length=50, blank=True)
    session_frequency = models.CharField(max_length=20, choices=SESSION_FREQUENCY_CHOICES, blank=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, blank=True)
    location_details = models.CharField(max_length=255, blank=True)
    tags = TaggableManager(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (self.looking_for_players or self.looking_for_dm):
            raise ValidationError("You can not post an ad without looking for at least 1 player.")
        if self.looking_for_players is False:
            self.num_players = None

    def save(self, *args, **kwargs):
        # Default title if blank
        if not self.title:
            self.title = f"{self.owner.username}'s ad"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title