from django.db.models.signals import post_save
from django.dispatch import receiver
from ad_applications.models import Application
from invitations.models import Invitation

@receiver(post_save, sender=Application)
def send_invitation_on_acceptance(sender, instance, created, **kwargs):
    # Only trigger if status is 'accepted' and no invitation exists yet
    if instance.status == 'accepted':
        invitation_exists = Invitation.objects.filter(application=instance).exists()
        if not invitation_exists:
            Invitation.objects.create(
                ad=instance.ad,
                application=instance,
                sender=instance.ad.owner, # or whichever field is correct
                recipient=instance.owner,  # or whichever field is correct
                status='pending'
            )