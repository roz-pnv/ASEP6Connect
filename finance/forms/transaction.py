from django import forms

from finance.models.transaction import TransactionType
from finance.models.transaction import TransactionStatus
from finance.models.transaction import PaymentMethod

class TransactionFilterForm(forms.Form):
    user_query = forms.CharField(
        required=False,
        label="User Name Contains"
    )
    type = forms.ChoiceField(
        choices=[('', 'All')] + list(TransactionType.choices),
        required=False,
        label="Type"
    )
    status = forms.ChoiceField(
        choices=[('', 'All')] + list(TransactionStatus.choices),
        required=False,
        label="Status"
    )
    payment_method = forms.ChoiceField(
        choices=[('', 'All')] + list(PaymentMethod.choices),
        required=False,
        label="Method"
    )