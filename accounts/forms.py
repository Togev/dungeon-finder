from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()


class BaseUserForm(forms.ModelForm):
    username = forms.CharField(
        help_text="Choose a unique username for logging in.",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        help_text="Please enter a valid email address.",
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    age = forms.IntegerField(
        required=True,
        help_text="You must be at least 18 years old to register.",
        widget=forms.NumberInput(attrs={'placeholder': 'Age'})
    )
    first_name = forms.CharField(
        required=True,
        help_text="Please enter your first name.",
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        help_text="Please enter your last name.",
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class UserRegistrationForm(UserCreationForm, BaseUserForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        help_text="Choose a strong password."
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}),
        help_text="Enter the same password as before, for verification."
    )

    class Meta(BaseUserForm.Meta):
        model = User
        fields = BaseUserForm.Meta.fields + ("password1", "password2")

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Remember me")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class UserDetailForm(BaseUserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        help_text="Edit your username.",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        required=True,
        help_text="Edit your email address.",
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    age = forms.IntegerField(
        required=True,
        help_text="Edit your age.",
        widget=forms.NumberInput(attrs={'placeholder': 'Age'})
    )
    first_name = forms.CharField(
        required=True,
        help_text="Edit your first name.",
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=True,
        help_text="Edit your last name.",
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "age", "first_name", "last_name")


class ProfileEditForm(forms.ModelForm):
    phone_number = forms.CharField(
        required=False,
        help_text="Enter your phone number.",
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )
    address = forms.CharField(
        required=False,
        help_text="Enter your address.",
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    about_me = forms.CharField(
        required=False,
        help_text="Tell us about yourself.",
        widget=forms.Textarea(attrs={'placeholder': 'About Me', 'rows': 4})
    )
    show_names = forms.BooleanField(
        required=False,
        help_text="Show your first and last name on your profile."
    )

    class Meta:
        model = Profile
        fields = ("phone_number", "address", "about_me", "profile_pic", "show_names")
        widgets = {
            'profile_pic': forms.FileInput,  # This removes the "clear" checkbox!
        }

