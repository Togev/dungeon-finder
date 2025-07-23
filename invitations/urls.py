from django.urls import path

from invitations.views import AcceptInvitationView, DeclineInvitationView

urlpatterns = [
    # path('send/<int:ad_id>/<int:application_id>/', SendInvitationView.as_view(), name='send_invitation'),
    path('accept/<int:invitation_id>/', AcceptInvitationView.as_view(), name='accept_invitation'),
    path('decline/<int:invitation_id>/', DeclineInvitationView.as_view(), name='decline_invitation'),
]