from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseNotAllowed
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from table_messages.models import TableMessage


# Create your views here.
class TableMessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TableMessage
    context_object_name = 'message'

    def get_success_url(self):
        return reverse_lazy('table_details', kwargs={'pk': self.object.table.pk})

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        table = obj.table

        is_message_sender = (user == obj.sender)
        is_table_owner = (user == table.created_by)
        is_table_admin = (user in table.admins.all())

        return is_message_sender or is_table_owner or is_table_admin

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])