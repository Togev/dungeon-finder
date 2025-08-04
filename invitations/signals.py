from django.db.models.signals import post_save
from django.dispatch import receiver
from ad_applications.models import Application
from invitations.models import Invitation

#   Triggers when an application is accepted

@receiver(post_save, sender=Application)
def send_invitation_on_acceptance(sender, instance, created, **kwargs):
    if instance.status == 'accepted':
        invitation_exists = Invitation.objects.filter(application=instance).exists()
        if not invitation_exists:
            Invitation.objects.create(
                ad=instance.ad,
                application=instance,
                sender=instance.ad.owner,
                recipient=instance.owner,
                status='pending'
            )