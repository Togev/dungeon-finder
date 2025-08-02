from django import forms
from .models import Table

class CreateTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'announcement']
        widgets = {
            'announcement': forms.Textarea(attrs={'rows': 4}),
        }

class ManageTableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'announcement', 'owner_color', 'admin_color', 'member_color']
        widgets = {
            'announcement': forms.Textarea(attrs={'rows': 4}),
            'owner_color': forms.TextInput(attrs={'type': 'color'}),
            'admin_color': forms.TextInput(attrs={'type': 'color'}),
            'member_color': forms.TextInput(attrs={'type': 'color'}),
        }

class TableAdminForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = "__all__"
        widgets = {
            "owner_color": forms.TextInput(attrs={"type": "color"}),
            "admin_color": forms.TextInput(attrs={"type": "color"}),
            "member_color": forms.TextInput(attrs={"type": "color"}),
        }