from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models.user import User
from users.models.user import Country

class SimpleRegistrationForm(UserCreationForm):
    country_of_origin = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=True,
        help_text="Select your country of origin"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username', 
            'email', 
            'country_of_origin', 
            'password1', 
            'password2'
        ]
