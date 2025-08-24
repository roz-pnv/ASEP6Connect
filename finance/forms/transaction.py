from django import forms

from finance.models.transaction import Transaction
from finance.models.transaction import TransactionType
from finance.models.transaction import TransactionStatus
from finance.models.transaction import PaymentMethod
from users.models import Membership
from users.models.membership import MemberType

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

    member_type = forms.ChoiceField(
        choices=[('', 'All')] + list(MemberType.choices),
        required=False,
        label="Membership Type"
    )

    is_student = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Student'), ('false', 'Non-Student')],
        required=False,
        label="Student Status"
    )


class TransactionPurposeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'note']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Optional note',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        transaction_type = kwargs.pop('transaction_type', None)
        wallet = kwargs.pop('wallet', None)
        super().__init__(*args, **kwargs)

        self.fields['type'].label = "Transaction Type"
        self.fields['note'].label = "Note"

        if transaction_type:
            self.fields['type'].initial = transaction_type
            self.fields['type'].disabled = True


class TransactionMethodForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['payment_method', 'amount']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount'
            }),
        }

    def __init__(self, *args, **kwargs):
        transaction_type = kwargs.pop('transaction_type', None)
        wallet = kwargs.pop('wallet', None)
        super().__init__(*args, **kwargs)

        self.fields['payment_method'].label = "Payment Method"
        
        if wallet and transaction_type:
            data = kwargs.get("initial", {})
            session_data = kwargs.get("data", {})
            
            amount = session_data.get("amount") or data.get("amount")
            if amount:
                self.fields['amount'].initial = amount
                self.fields['amount'].disabled = True

        allowed = [PaymentMethod.WALLET, PaymentMethod.ONLINE]
        
        self.fields['payment_method'].choices = [
			(key, label) for key, label in self.fields['payment_method'].choices
			if key in allowed
		]

    def clean_amount(self):
        if self.fields['amount'].disabled:
            return self.initial.get('amount')
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount


class VerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter verification code'
        })
    )

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit():
            raise forms.ValidationError("Code must be numeric.")
        if len(code) != 6:
            raise forms.ValidationError("Code must be 6 digits.")
        return code
