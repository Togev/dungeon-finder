from django import forms
from .models import Ad

class CreateAdForm(forms.ModelForm):
    create_table = forms.BooleanField(required=False, label="Create a table for this ad")

    class Meta:
        model = Ad
        fields = [
            'title',
            'description',
            'looking_for_players',
            'looking_for_dm',
            'num_players',
            'game_system',
            'session_frequency',
            'location_type',
            'location_details',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            # The default taggit widget is a simple text input for comma-separated tags
        }

    def clean(self):
        cleaned_data = super().clean()
        looking_for_players = cleaned_data.get('looking_for_players')
        looking_for_dm = cleaned_data.get('looking_for_dm')
        num_players = cleaned_data.get('num_players')

        # Require at least one of looking_for_players or looking_for_dm
        if not (looking_for_players or looking_for_dm):
            raise forms.ValidationError(
                "You must be looking for at least a player or a DM."
            )

        # Only allow num_players if looking_for_players is checked
        if not looking_for_players:
            cleaned_data['num_players'] = None
        elif looking_for_players and (num_players is None or num_players < 1):
            raise forms.ValidationError(
                "Please specify how many players you are looking for."
            )

        return cleaned_data

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 10:
            raise forms.ValidationError("You can add up to 10 tags only.")
        return tags


class EditAdForm(CreateAdForm):
    pass

