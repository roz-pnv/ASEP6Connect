from django import forms

from meetings.models import AgendaItem

class AgendaItemForm(forms.ModelForm):
    class Meta:
        model = AgendaItem
        fields = '__all__'
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'requires_vote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'meeting': 'Meeting',
            'title': 'Title',
            'description': 'Description',
            'order': 'Order',
            'file': 'Attachment',
            'requires_vote': 'Requires Vote',
        }
