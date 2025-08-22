from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model

from meetings.models.meeting import Meeting
from meetings.models.agenda import AgendaItem

User = get_user_model()

class MeetingForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    class Meta:
        model = Meeting
        fields = [
            'title', 
            'meeting_type', 
            'date', 
            'location', 
            'online_link',
        ]

AgendaItemFormSet = inlineformset_factory(
    Meeting, AgendaItem,
    fields=[
		'title', 
        'description', 
        'order', 
        'file', 
        'requires_vote',
    ],
    extra=1, can_delete=True
)


class InviteUsersForm(forms.Form):
    invited_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_invited_users'}),
        required=False,
        label="Invite Users"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invited_users'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({'Board' if obj.is_boardofdirector else 'Member'})"


class MeetingUpdateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'title': 'Meeting Title',
            'date': 'Date & Time',
            'location': 'Location',
            'description': 'Description',
        }
