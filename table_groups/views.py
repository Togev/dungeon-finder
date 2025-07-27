from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import FormMixin

from table_messages.forms import TableMessageForm
from .forms import CreateTableForm, ManageTableForm
from .models import Table

class MyTablesListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'table_groups/my_tables.html'
    paginate_by = 5

    def get_queryset(self):
        return Table.objects.filter(
            members=self.request.user
        ).order_by('-created_at').distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role_map = {}
        for table in context['page_obj']:
            if table.created_by == user:
                role = "Creator"
            elif table.admins.filter(pk=user.pk).exists():
                role = "Admin"
            elif table.members.filter(pk=user.pk).exists():
                role = "Member"
            else:
                role = "Unknown"
            role_map[table.pk] = role
        context['role_map'] = role_map
        return context

class CreateTableView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = CreateTableForm
    template_name = 'table_groups/create_table.html'
    success_url = reverse_lazy('my_tables')

    def form_valid(self, form):
        # Set creator as the current user
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Add creator as a member (but not admin)
        self.object.members.add(self.request.user)
        return response

class TableDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Table
    template_name = 'table_groups/table_details.html'
    context_object_name = 'table'
    form_class = TableMessageForm

    def get_success_url(self):
        return reverse('table_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.order_by('-sent_at')
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            message = form.save(commit=False)
            message.table = self.object
            message.sender = self.request.user
            message.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ManageTableView(LoginRequiredMixin, UpdateView):
    model = Table
    form_class = ManageTableForm
    template_name = 'table_groups/manage_table.html'

    def get_object(self, queryset=None):
        table = get_object_or_404(Table, id=self.kwargs['pk'])
        user = self.request.user
        if user != table.created_by and user not in table.admins.all():
            return HttpResponseForbidden("You do not have permission to manage this table.")
        return table

    def get_success_url(self):
        return reverse_lazy('manage_table', kwargs={'pk': self.object.pk})
