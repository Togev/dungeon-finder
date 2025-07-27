from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Invitation
from ads.models import Ad
from ad_applications.models import Application


# Has been converted into a signal, executing upon Application Accept, kept for here just in case

# class SendInvitationView(LoginRequiredMixin, View):
#     def post(self, request, ad_id, application_id):
#         ad = get_object_or_404(Ad, id=ad_id, owner=request.user)
#         application = get_object_or_404(Application, id=application_id)
#         receiver = application.owner
#
#         invitation, created = Invitation.objects.get_or_create(
#             ad=ad,
#             application=application,
#             sender=request.user,
#             recipient=receiver,
#             defaults={'status': 'pending'}
#         )
#         return redirect('application_details', pk=application.id)

class AcceptInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id, recipient=request.user)
        if invitation.status == 'pending':
            invitation.status = 'accepted'
            invitation.responded_at = timezone.now()
            invitation.save()
            table = invitation.ad.table
            table.members.add(request.user)
            messages.success(request, "Invitation accepted.")
        else:
            messages.error(request, f"Invitation has already been {invitation.status}. You cannot change your response.")
        return redirect('my_applications')

class DeclineInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(Invitation, id=invitation_id, recipient=request.user)
        if invitation.status == 'pending':
            invitation.status = 'declined'
            invitation.responded_at = timezone.now()
            invitation.save()
            messages.success(request, "Invitation declined.")
        else:
            messages.error(request, f"Invitation has already been {invitation.status}. You cannot change your response.")
        return redirect('my_applications')