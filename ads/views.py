from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

from ad_applications.models import Application
from table_groups.models import Table
from .models import Ad
from .forms import CreateAdForm, EditAdForm

# Ad List view is located in common/views as it affects which landing page is displayed if logged in

class CreateAdView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = CreateAdForm
    template_name = 'ads/create_ad.html'
    success_url = reverse_lazy('landing_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user

        table = form.cleaned_data['table']
        new_name = form.cleaned_data.get('new_table_name')
        new_desc = form.cleaned_data.get('new_table_description')

        if table == '__new__':
            # Safe to assume both name and description are valid due to form validation
            table = Table.objects.create(
                name=new_name,
                description=new_desc,
                created_by=self.request.user
            )

        form.instance.table = table  # Either the new one or existing instance

        return super().form_valid(form)

class EditAdView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = EditAdForm  # Or CreateAdForm if they're identical
    template_name = 'ads/edit_ad.html'  # Reuse the same form template

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('ad_details', args=[self.object.pk])
    # Adjust to your ad listing url name

    def get_queryset(self):
        # Optional: restrict editing so users can only edit their own ads
        return super().get_queryset().filter(owner=self.request.user)


class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad
    template_name = 'ads/view_ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        # Check if the logged-in user has already applied
        user_application = Application.objects.filter(ad=ad, owner=self.request.user).first()
        context['user_application'] = user_application
        return context

class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/delete_ad.html'
    success_url = reverse_lazy('landing_page')

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

class MyAdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/my_ads.html'
    paginate_by = 5

    def get_queryset(self):
        return Ad.objects.filter(owner=self.request.user).order_by('-created')