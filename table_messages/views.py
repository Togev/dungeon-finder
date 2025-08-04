from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.test_func():
            return JsonResponse({'success': False, 'error': 'Permission denied.'}, status=403) if request.headers.get('x-requested-with') == 'XMLHttpRequest' else HttpResponseRedirect(self.get_success_url())
        self.object.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return HttpResponseRedirect(self.get_success_url())