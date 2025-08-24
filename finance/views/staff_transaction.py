from django.db.models import Q
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.timezone import now

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction
from finance.models.transaction import TransactionType
from users.models import Membership
from users.models.board_of_director import BoardOfDirector, RoleType
from users.views.staff_panel import BoardRoleContextMixin
from finance.forms.transaction import TransactionFilterForm
    
Users = get_user_model()


class TransactionAdminView(BoardRoleContextMixin, UserPassesTestMixin, TemplateView):
    """
    Admin view for treasurers to monitor and filter transactions across all wallets.
    Includes filters for user identity, transaction details, membership type, and student status.
    """
    template_name = "finance_staff_panel/transaction_list.html"

    def test_func(self):
        # Access restricted to users with active treasurer role
        role = BoardOfDirector.objects.filter(user=self.request.user).order_by('-start_date').first()
        return role and role.role_type == RoleType.TREASURER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Base queryset: all transactions with related wallet, user, and membership
        transactions = Transaction.objects.select_related("wallet", "wallet__user", "membership").order_by("-created_at")
        wallets = Wallet.objects.select_related("user").order_by("-created_at")

        # Apply filters from form
        form = TransactionFilterForm(self.request.GET or None)
        if form.is_valid():
            cd = form.cleaned_data

            # Filter by user name or username
            if cd.get("user_query"):
                q = cd["user_query"]
                transactions = transactions.filter(
                    Q(wallet__user__username__icontains=q) |
                    Q(wallet__user__first_name__icontains=q) |
                    Q(wallet__user__last_name__icontains=q)
                )

            # Filter by transaction type
            if cd.get("type"):
                transactions = transactions.filter(type=cd["type"])

            # Filter by transaction status
            if cd.get("status"):
                transactions = transactions.filter(status=cd["status"])

            # Filter by payment method
            if cd.get("payment_method"):
                transactions = transactions.filter(payment_method=cd["payment_method"])

            # Filter by membership type (active and not expired)
            if cd.get("member_type"):
                transactions = transactions.filter(
                    membership__member_type=cd["member_type"],
                    membership__is_active=True,
                    membership__membership_expiry__gte=timezone.now()
                )

            # Filter by student status
            if cd.get("is_student") == "true":
                transactions = transactions.filter(wallet__user__is_student=True)
            elif cd.get("is_student") == "false":
                transactions = transactions.filter(wallet__user__is_student=False)

        context.update({
            "wallets": wallets,
            "transactions": transactions.distinct()[:50],
            "filter_form": form,
        })
        return context
    

class TransactionReceiptView(BoardRoleContextMixin, TemplateView):
    template_name = "finance_staff_panel/transaction_receipt.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_id = self.kwargs.get("transaction_id")
        transaction = get_object_or_404(
            Transaction.objects.select_related("wallet", "wallet__user", "membership"),
            id=transaction_id
        )

        membership = transaction.membership
        show_confirm_button = (
            transaction.type == TransactionType.MEMBERSHIP_FEE
            and membership is not None
            and not membership.is_confirmed
        )

        context.update({
            "transaction": transaction,
            "wallet": transaction.wallet,
            "membership": membership,
            "show_confirm_button": show_confirm_button
        })
        return context
    
	
class ConfirmMembershipView(View):
    def post(self, request, membership_id):
        membership = get_object_or_404(Membership, id=membership_id)

        # Confirm membership and enable voting
        membership.is_confirmed = True
        membership.can_vote = True
        membership.confirmed_at = now()
        membership.save()

        messages.success(request, "Membership confirmed and voting rights enabled.")

        # Redirect to the related transaction receipt
        transaction = Transaction.objects.filter(membership=membership).order_by('-created_at').first()
        if transaction:
            return redirect("transaction_receipt", transaction_id=transaction.id)
        return redirect("admin_dashboard")
