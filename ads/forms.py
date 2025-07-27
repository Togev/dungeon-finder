from django import forms

from table_groups.models import Table
from .models import Ad

class TableChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        if value in (None, '', 'None'):
            return None
        if value == '__new__':
            return '__new__'
        return super().to_python(value)

    def validate(self, value):
        if value == '__new__':
            return
        super().validate(value)


class CreateAdForm(forms.ModelForm):
    table = TableChoiceField(
        queryset=Table.objects.none(),
        required=False,
        label="Select an existing Table Group"
    )
    new_table_name = forms.CharField(
        required=False,
        label="New Table Group Name"
    )
    new_table_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        label="New Table Group Description"
    )

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
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            available_tables = Table.objects.filter(created_by=user, ad__isnull=True)
            self.fields['table'].queryset = available_tables
            self.no_existing_tables = not available_tables.exists()

    def clean_table(self):
        value = self.cleaned_data.get('table')
        if value is None:
            raise forms.ValidationError(
                "You must select an existing Table Group or choose 'Create new table' and fill in its details."
            )
        return value

    def _validate_new_table_fields(self, new_name):
        if not new_name:
            self.add_error('new_table_name', "Please provide a name for the new Table Group.")
        raise forms.ValidationError("You must provide details for a new Table Group.")

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        new_name = cleaned_data.get('new_table_name')

        if self.no_existing_tables:
            if not new_name:
                self._validate_new_table_fields(new_name)
        else:
            if table == '__new__':
                if not new_name:
                    self._validate_new_table_fields(new_name)
            else:
                if new_name:
                    self.add_error(
                        'table',
                        "You cannot select an existing Table Group and also provide details for a new one."
                    )

        looking_for_players = cleaned_data.get('looking_for_players')
        looking_for_dm = cleaned_data.get('looking_for_dm')
        num_players = cleaned_data.get('num_players')

        if not (looking_for_players or looking_for_dm):
            raise forms.ValidationError(
                "You must be looking for at least a player or a DM."
            )

        if not looking_for_players:
            cleaned_data['num_players'] = None
        elif looking_for_players and (num_players is None or num_players < 1):
            raise forms.ValidationError(
                "Please specify how many players you are looking for."
            )

        return cleaned_data

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 5:
            raise forms.ValidationError("You can add up to 5 tags only.")
        return tags

class EditAdForm(CreateAdForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields.pop('table', None)
        self.fields.pop('new_table_name', None)
        self.fields.pop('new_table_description', None)

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        looking_for_players = cleaned_data.get('looking_for_players')
        looking_for_dm = cleaned_data.get('looking_for_dm')
        num_players = cleaned_data.get('num_players')

        if not (looking_for_players or looking_for_dm):
            raise forms.ValidationError(
                "You must be looking for at least a player or a DM."
            )

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