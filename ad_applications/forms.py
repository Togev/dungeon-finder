from django import forms
from .models import Application

class ApplicationCreateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['role', 'message']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'role': "I'm looking to be a...:",
            'message': "Tell us about yourself",
        }
