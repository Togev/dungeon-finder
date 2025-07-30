from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MinValueValidator

from django.conf import settings
from accounts.validators import UsernameAlphaNumericUnderscoreValidator
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
    max_length=30,
    unique=True,
    validators=[MinLengthValidator(4, message="Username must be at least 4 characters long"),
                UsernameAlphaNumericUnderscoreValidator],
    error_messages={
        "unique": "A user with that username already exists.",
    },
    help_text="Required. 4-30 characters long. Must start with a letter and contain only letters, numbers and underscores.",
)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message="You must be at least 18 years old to register.")],
        help_text="You must be at least 18 years old to register.",
    )

    def __str__(self):
        return self.username

def user_profile_pic_path(instance, filename):
    return f"profile_pics/{instance.user.pk}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=user_profile_pic_path, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)
    show_names = models.BooleanField(default=True, help_text="Show your first and last name on your profile.")

    def __str__(self):
        return f"{self.user.username}'s profile"