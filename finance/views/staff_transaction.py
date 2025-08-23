from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction
from users.models.board_of_director import BoardOfDirector, RoleType
from users.views.staff_panel import BoardRoleContextMixin
from finance.forms.transaction import TransactionFilterForm


class TransactionAdminView(BoardRoleContextMixin, UserPassesTestMixin, TemplateView):
    """
    Treasurer-only view to list and filter transactions across all wallets.
    """
    template_name = "finance_staff_panel/transaction_list.html"

    def test_func(self):
        # Only allow access if user is an active treasurer
        active_role = (
            BoardOfDirector.objects.filter(user=self.request.user)
            .order_by('-start_date')
            .first()
        )
        return active_role and active_role.role_type == RoleType.TREASURER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Base queryset: all transactions with related wallet and membership
        transactions = Transaction.objects.select_related("wallet", "wallet__user", "membership").order_by("-created_at")

        # Wallets for sidebar or context (optional)
        wallets = Wallet.objects.select_related("user").order_by("-created_at")

        # Apply filters
        form = TransactionFilterForm(self.request.GET or None)
        if form.is_valid():
            cd = form.cleaned_data

            # Filter by user query (username, first name, last name)
            if cd.get("user_query"):
                q = cd["user_query"]
                transactions = transactions.filter(
                    Q(wallet__user__username__icontains=q) |
                    Q(wallet__user__first_name__icontains=q) |
                    Q(wallet__user__last_name__icontains=q)
                )

            # Filter by type, status, payment method
            if cd.get("type"):
                transactions = transactions.filter(type=cd["type"])
            if cd.get("status"):
                transactions = transactions.filter(status=cd["status"])
            if cd.get("payment_method"):
                transactions = transactions.filter(payment_method=cd["payment_method"])

        # Final context
        context.update({
            "wallets": wallets,
            "transactions": transactions[:50],  # Limit for performance
            "filter_form": form,
        })
        return context
