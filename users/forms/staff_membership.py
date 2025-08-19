from django import forms
from django.utils import timezone
from users.models import Membership

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = [
            "member_type",
            "can_vote",
            "is_active",
            "is_confirmed",
            "membership_expiry",
        ]
        widgets = {
            "membership_expiry": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        membership = super().save(commit=False)

        if membership.pk:
            previous = Membership.objects.get(pk=membership.pk)
            was_confirmed = previous.is_confirmed
        else:
            was_confirmed = False

        if self.cleaned_data.get("is_confirmed") and not was_confirmed:
            membership.confirmed_at = timezone.now()
        elif not self.cleaned_data.get("is_confirmed"):
            membership.confirmed_at = None

        if commit:
            membership.save()
        return membership
