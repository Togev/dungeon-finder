import requests
from django.core.files.base import ContentFile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Profile
import os
import shutil

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_and_avatar(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        # Save avatar in user-specific folder
        name = f"{instance.first_name}+{instance.last_name}"
        if not instance.first_name and not instance.last_name:
            name = instance.username
        avatar_url = f"https://ui-avatars.com/api/?name={name}&size=150&rounded=true"
        response = requests.get(avatar_url)
        if response.status_code == 200:
            avatar_filename = f"{instance.pk}_avatar.png"
            profile.profile_pic.save(
                avatar_filename,
                ContentFile(response.content),
                save=True
            )

@receiver(post_delete, sender=User)
def delete_user_profile_pics_folder(sender, instance, **kwargs):
    # Remove user's profile pics folder when the user is deleted
    user_folder = os.path.join(settings.MEDIA_ROOT, "profile_pics", str(instance.pk))
    if os.path.isdir(user_folder):
        shutil.rmtree(user_folder)