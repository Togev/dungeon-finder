from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView, TemplateView
from django.views.generic.edit import FormMixin

from accounts.models import CustomUser
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

class TableDemoteAdminView(LoginRequiredMixin, View):
    def post(self, request, pk, member_id):
        table = get_object_or_404(Table, id=pk)
        member = get_object_or_404(CustomUser, id=member_id)

        if request.user != table.created_by:
            messages.error(request, "Only the table owner can demote admins.")
            return redirect('manage_table', pk=table.pk)

        if member == table.created_by:
            messages.error(request, "You cannot demote the table owner.")
            return redirect('manage_table', pk=table.pk)
        if member not in table.admins.all():
            messages.error(request, f"{member.username} is not an admin.")
            return redirect('manage_table', pk=table.pk)

        table.admins.remove(member)
        messages.success(request, f"{member.username} has been demoted to member.")
        return redirect('manage_table', pk=table.pk)

class TablePromoteAdminView(LoginRequiredMixin, View):
    def post(self, request, pk, member_id):
        table = get_object_or_404(Table, id=pk)
        member = get_object_or_404(CustomUser, id=member_id)

        if request.user != table.created_by:
            messages.error(request, "Only the table owner can promote admins.")
            return redirect('manage_table', pk=table.pk)

        if member == table.created_by:
            messages.error(request, "The owner is already an admin.")
            return redirect('manage_table', pk=table.pk)
        if member in table.admins.all():
            messages.error(request, f"{member.username} is already an admin.")
            return redirect('manage_table', pk=table.pk)
        if member not in table.members.all():
            messages.error(request, f"{member.username} is not a member of this table.")
            return redirect('manage_table', pk=table.pk)

        table.admins.add(member)
        messages.success(request, f"{member.username} has been promoted to admin.")
        return redirect('manage_table', pk=table.pk)

class TableRemoveMemberView(LoginRequiredMixin, View):
    def post(self, request, pk, member_id):
        table = get_object_or_404(Table, id=pk)
        member = get_object_or_404(CustomUser, id=member_id)

        if request.user != table.created_by and request.user not in table.admins.all():
            messages.error(request, "You do not have permission to remove members from this table.")
            return redirect('manage_table', pk=table.pk)

        if member == table.created_by:
            messages.error(request, "You cannot remove the table owner.")
            return redirect('manage_table', pk=table.pk)

        if member not in table.members.all():
            messages.error(request, f"{member.username} is not a member of this table.")
            return redirect('manage_table', pk=table.pk)

        table.members.remove(member)
        table.admins.remove(member)
        messages.success(request, f"{member.username} has been removed from the table.")
        return redirect('manage_table', pk=table.pk)

class TableTransferOwnershipView(LoginRequiredMixin, View):
    def get(self, request, pk, member_id):
        table = get_object_or_404(Table, id=pk)
        member = get_object_or_404(CustomUser, id=member_id)

        if request.user != table.created_by:
            messages.error(request, "Only the current owner can transfer ownership.")
            return redirect('manage_table', pk=table.pk)

        if member == table.created_by:
            messages.error(request, "You are already the owner.")
            return redirect('manage_table', pk=table.pk)

        if member not in table.members.all():
            messages.error(request, "Can only transfer ownership to a table member.")
            return redirect('manage_table', pk=table.pk)

        return render(request, "table_groups/confirm_transfer_ownership.html", {
            "table": table,
            "member": member,
        })

    def post(self, request, pk, member_id):
        table = get_object_or_404(Table, id=pk)
        member = get_object_or_404(CustomUser, id=member_id)

        if request.user != table.created_by:
            messages.error(request, "Only the current owner can transfer ownership.")
            return redirect('manage_table', pk=table.pk)

        if member == table.created_by:
            messages.error(request, "You are already the owner.")
            return redirect('manage_table', pk=table.pk)

        if member not in table.members.all():
            messages.error(request, "Can only transfer ownership to a table member.")
            return redirect('manage_table', pk=table.pk)

        table.created_by = member
        table.admins.remove(member)
        table.save()
        messages.success(request, f"Ownership transferred to {member.username}.")
        return redirect('table_details', pk=table.pk)

class TableDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Table
    template_name = "table_groups/delete_table.html"
    context_object_name = "table"
    success_url = reverse_lazy("my_tables")

    def test_func(self):
        table = self.get_object()
        return self.request.user == table.created_by

class TableLeaveView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "table_groups/leave_table.html"
    success_url = reverse_lazy("my_tables")  # Redirect wherever appropriate

    def dispatch(self, request, *args, **kwargs):
        self.table = get_object_or_404(Table, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        user = self.request.user
        table = self.table
        is_admin = user in table.admins.all()
        is_member = user in table.members.all()
        is_owner = user == table.created_by
        return not is_owner and (is_admin or is_member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.table
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        table = self.table
        if user in table.admins.all():
            table.admins.remove(user)
        if user in table.members.all():
            table.members.remove(user)
        return redirect(self.success_url)