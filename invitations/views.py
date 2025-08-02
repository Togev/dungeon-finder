from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Invitation


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