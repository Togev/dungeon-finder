from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .forms import UserRegistrationForm, CustomAuthenticationForm, UserDetailForm, UserEditForm, ProfileEditForm
from django.urls import reverse_lazy, reverse

from accounts.models import CustomUser

# Create your views here.
User = get_user_model()

class RegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "accounts/registration_page.html"
    success_url = reverse_lazy('landing_page')  #  triggers signal to create Profile model related to User and assign default pic from ui-avatars.com

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        return response

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        REMEMBER_ME_SESSION_DURATiON = 1209600
        NOT_REMEMBER_ME_SESSION_DURATION = 0

        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(NOT_REMEMBER_ME_SESSION_DURATION)
        else:
            self.request.session.set_expiry(REMEMBER_ME_SESSION_DURATiON)
        return super().form_valid(form)

class UserDetailView(DetailView):
    model = User
    template_name = "accounts/account_details.html"
    context_object_name = "profile_user"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['is_owner'] = self.request.user == user
        context['form'] = UserDetailForm(instance=user)
        context['profile'] = getattr(user, 'profile', None)
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'user_obj'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        user_obj = get_object_or_404(User, pk=self.kwargs.get('pk'))
        if self.request.user != user_obj:
            return HttpResponseForbidden("You do not have permission to edit this profile.")
        return user_obj

    def get_profile(self):
        return self.get_object().profile

    def get_success_url(self) -> str:
        return reverse(
            'account_details',
            kwargs={
                'pk': self.object.pk,
            }
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.form_class(instance=self.object)
        profile_form = ProfileEditForm(instance=self.get_profile())
        return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.form_class(request.POST, instance=self.object)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=self.get_profile())
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect('account_details', pk=self.object.pk)
        else:
            messages.error(request, "Please correct the errors below.")
            return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('user_form', kwargs.get('user_form'))
        context.setdefault('profile_form', kwargs.get('profile_form'))
        return context

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('landing_page')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj:
            raise PermissionDenied("You do not have permission to delete this account.")
        return obj

