from django import forms

from finance.models.transaction import TransactionType
from finance.models.transaction import PaymentMethod
from users.models import Membership


class TransactionPurposeForm(forms.Form):
    type = forms.ChoiceField(choices=TransactionType.choices, label="Transaction Type")
    note = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Note")
    

class TransactionMethodForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PaymentMethod.choices, label="Payment Method")
    amount = forms.IntegerField(min_value=1, label="Amount")

    def __init__(self, *args, transaction_type=None, wallet=None, **kwargs):
        super().__init__(*args, **kwargs)

        if transaction_type == "membership_fee" and wallet:
            self.fields["membership"] = forms.ModelChoiceField(
                queryset=Membership.objects.filter(user=wallet.user),
                required=True,
                label="Select Membership",
                help_text="Choose the membership this transaction is for"
            )
            
class TransactionExtraForm(forms.Form):
    related_project = forms.CharField(max_length=255, required=False, label="Related Project")


class VerificationForm(forms.Form):
    verification_code = forms.IntegerField(
        min_value=100000, 
        max_value=999999,
        label='Enter verification code'
    )