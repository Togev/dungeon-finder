from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from invitations.models import Invitation
from .models import Application
from .forms import ApplicationCreateForm
from ads.models import Ad


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationCreateForm
    template_name = 'ad_applications/application_create.html'
    success_url = reverse_lazy('my_applications')

    def dispatch(self, request, *args, **kwargs):
        self.ad = get_object_or_404(Ad, pk=self.kwargs['ad_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        application = form.save(commit=False)
        application.ad = self.ad
        application.owner = self.request.user
        application.recipient = self.ad.owner
        application.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = self.ad
        return context

class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'ad_applications/application_details.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application = context['application']
        invitation = Invitation.objects.filter(application=application).first()
        context['invitation'] = invitation
        return context

class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    template_name = 'ad_applications/application_delete.html'
    success_url = reverse_lazy('my_applications')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class ApplicationAcceptView(LoginRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        if application.recipient != request.user:
            return PermissionDenied
        if application.status != 'pending':
            messages.error(request, "Status has already been set and cannot be changed.")
            return redirect('application_details', pk=application.pk)
        application.status = 'accepted'
        application.save()
        return redirect('my_applications')

class ApplicationRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        if application.recipient != request.user:
            return PermissionDenied
        if application.status != 'pending':
            messages.error(request, "Status has already been set and cannot be changed.")
            return redirect('application_details', pk=application.pk)
        application.status = 'rejected'
        application.save()
        return redirect('my_applications')

class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'ad_applications/my_applications.html'
    context_object_name = 'applications'
    paginate_by = 5

    def get_queryset(self):
        view_type = self.request.GET.get('type', 'sent')
        user = self.request.user
        if view_type == 'received':
            return Application.objects.filter(recipient=user).order_by('-submitted_at')
        return Application.objects.filter(owner=user).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_type'] = self.request.GET.get('type', 'sent')
        applications = context['applications']

        for app in applications:
            app.invitation = Invitation.objects.filter(application=app).first()

        context['applications'] = applications
        context['user'] = self.request.user
        return context


