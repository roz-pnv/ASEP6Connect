from django import forms
from meetings.models.motion import Motion
from meetings.models.agenda import AgendaItem

class MotionCreateForm(forms.ModelForm):
    class Meta:
        model = Motion
        fields = ['agenda_item', 'text']
        widgets = {
            'agenda_item': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter motion text...'}),
        }
        labels = {
            'agenda_item': 'Agenda Item',
            'text': 'Motion Text'
        }

    def __init__(self, *args, **kwargs):
        meeting = kwargs.pop('meeting', None)
        super().__init__(*args, **kwargs)
        if meeting:
            self.fields['agenda_item'].queryset = AgendaItem.objects.filter(meeting=meeting)
