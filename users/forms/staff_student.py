from django import forms
from users.models.student import Student

class StudentForm(forms.ModelForm):
    arrival_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        required=False,
        label="Arrival Date"
    )

    class Meta:
        model = Student
        exclude = ["user"] 
        widgets = {
            "field_of_study": forms.TextInput(attrs={"class": "form-control"}),
            "accommodation_type": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "field_of_study": "Field of Study",
            "accommodation_type": "Accommodation Type",
            "arrival_date": "Arrival Date",
        }
