from django import forms

from users.models import User
from users.models import Student
from users.models.user import Country

class UserUpdateForm(forms.ModelForm):
    country_of_origin = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        help_text="Select your country of origin"
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'country_of_origin',
            'first_name', 
            'last_name', 
            'gender', 
            'job', 
            'phone', 
            'address', 
            'language', 
            'birthdate',
            'is_student',
        ]
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'field_of_study', 
            'arrival_date', 
            'accommodation_type', 
        ]
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
        }

