from django import forms

from meetings.models import Minutes

class MinutesForm(forms.ModelForm):
    class Meta:
        model = Minutes
        fields = '__all__'
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'recorded_by': forms.Select(attrs={'class': 'form-control'}),
            'approved_by': forms.Select(attrs={'class': 'form-control'}),
            'approved_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
