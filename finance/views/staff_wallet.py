from django.db.models import Q
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from finance.models.wallet import Wallet

from users.models.board_of_director import BoardOfDirector, RoleType
from users.views.staff_panel import BoardRoleContextMixin
from finance.forms.wallet import WalletFilterForm 

class WalletAdminView(BoardRoleContextMixin, UserPassesTestMixin, TemplateView):
    """
    Treasurer-only view to list all user wallets with optional filtering.
    """
    template_name = "finance_staff_panel/wallet_list.html"

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

        # Base queryset: all wallets with user info
        wallets = Wallet.objects.select_related("user").order_by("-created_at")

        # Apply filters if form is valid
        form = WalletFilterForm(self.request.GET or None)
        if form.is_valid():
            if form.cleaned_data.get("user_query"):
                q = form.cleaned_data["user_query"]
                wallets = wallets.filter(
					Q(user__username__icontains=q) |
					Q(user__first_name__icontains=q) |
					Q(user__last_name__icontains=q)
				)
            if form.cleaned_data.get("min_balance") is not None:
                wallets = wallets.filter(balance__gte=form.cleaned_data["min_balance"])
            if form.cleaned_data.get("max_balance") is not None:
                wallets = wallets.filter(balance__lte=form.cleaned_data["max_balance"])
            if form.cleaned_data.get("created_after"):
                wallets = wallets.filter(created_at__gte=form.cleaned_data["created_after"])
            if form.cleaned_data.get("created_before"):
                wallets = wallets.filter(created_at__lte=form.cleaned_data["created_before"])

        context.update({
            "wallets": wallets[:50],  # Limit for performance
            "filter_form": form,
        })
        return context
