from django import forms

from meetings.models import Invite

class InviteForm(forms.ModelForm):
    class Meta:
        model = Invite
        fields = '__all__'  
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-control'}),
            'invited_user': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'responded_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'meeting': 'Meeting',
            'invited_user': 'Invited User',
            'status': 'Response Status',
            'responded_at': 'Responded At',
            'message': 'Optional Message',
        }
