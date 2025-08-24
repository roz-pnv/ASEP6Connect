from django import forms

from users.models.membership import MemberType

class WalletFilterForm(forms.Form):
    """
    Filter form for admin wallet view.
    """
    user_query = forms.CharField(
		required=False,
		label="User Name Contains"
	)
    min_balance = forms.IntegerField(
        required=False,
        label="Min Balance"
    )
    max_balance = forms.IntegerField(
        required=False,
        label="Max Balance"
    )
    created_after = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created After"
    )
    created_before = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Created Before"
    )
    
    member_type = forms.ChoiceField(
        choices=[("", "----")] + list(MemberType.choices),
        required=False,
        label="Membership Type"
    )
    is_student = forms.ChoiceField(
        choices=[("", "----"), ("true", "student"), ("false", "non-student")],
        required=False,
        label="Student status"
    )
