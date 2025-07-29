from django import forms
from .models import TableMessage

class TableMessageForm(forms.ModelForm):
    class Meta:
        model = TableMessage
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }