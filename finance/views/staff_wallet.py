from django.db.models import Q
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction
from users.models import Membership 
from users.models.board_of_director import BoardOfDirector, RoleType
from finance.forms.wallet import WalletFilterForm
from finance.forms.transaction import TransactionFilterForm
from users.views.staff_panel import BoardRoleContextMixin


class WalletAdminView(BoardRoleContextMixin, UserPassesTestMixin, TemplateView):
    """ Treasurer-only view to list wallets and membership requests with unified filtering. """
    template_name = "finance_staff_panel/wallet_list.html"

    def test_func(self):
        role = BoardOfDirector.objects.filter(user=self.request.user).order_by('-start_date').first()
        return role and role.role_type == RoleType.TREASURER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = self.request.GET.get("target", "wallets")

        # ✅ Only one filter form is used, but passed twice for template compatibility
        filter_form = WalletFilterForm(self.request.GET or None, prefix="wallet")

        # Base queryset for wallets
        wallets = Wallet.objects.select_related("user").order_by("-created_at")

        # Base queryset for membership requests
        membership_request_wallets = Wallet.objects.select_related("user").filter(
            user__memberships__is_active=True,
            user__memberships__is_confirmed=False
        ).distinct()

        if filter_form.is_valid():
            cd = filter_form.cleaned_data
            if target == "wallets":
                wallets = self.apply_filters(wallets, cd)
            elif target == "requests":
                membership_request_wallets = self.apply_filters(membership_request_wallets, cd)

        # Membership maps
        latest_membership_map = {
            wallet.user.id: wallet.user.memberships.order_by('-created_at').first()
            for wallet in wallets
        }
        request_membership_map = {
            wallet.user.id: wallet.user.memberships.filter(
                is_active=True,
                is_confirmed=False
            ).order_by('-created_at').first()
            for wallet in membership_request_wallets
        }

        context.update({
            "wallets": wallets[:50],
            "membership_request_wallets": membership_request_wallets[:50],
            "latest_membership_map": latest_membership_map,
            "request_membership_map": request_membership_map,
            "wallet_filter_form": filter_form,  # ✅ same form used twice
            "request_filter_form": filter_form,
        })
        return context

    def apply_filters(self, queryset, cd):
        if cd.get("user_query"):
            q = cd["user_query"]
            queryset = queryset.filter(
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q)
            )
        if cd.get("min_balance") is not None:
            queryset = queryset.filter(balance__gte=cd["min_balance"])
        if cd.get("max_balance") is not None:
            queryset = queryset.filter(balance__lte=cd["max_balance"])
        if cd.get("created_after"):
            queryset = queryset.filter(created_at__gte=cd["created_after"])
        if cd.get("created_before"):
            queryset = queryset.filter(created_at__lte=cd["created_before"])
        if cd.get("member_type"):
            queryset = queryset.filter(
                user__memberships__member_type=cd["member_type"],
                user__memberships__is_active=True,
                user__memberships__membership_expiry__gte=timezone.now()
            )
        if cd.get("is_student") == "true":
            queryset = queryset.filter(user__is_student=True)
        elif cd.get("is_student") == "false":
            queryset = queryset.filter(user__is_student=False)
        return queryset


class WalletDetailAdminView(BoardRoleContextMixin, UserPassesTestMixin, TemplateView):
    template_name = "finance_staff_panel/wallet_detail.html"
    
    def test_func(self):
        role = BoardOfDirector.objects.filter(user=self.request.user).order_by('-start_date').first()
        return role and role.role_type == RoleType.TREASURER
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        wallet_id = self.kwargs.get("wallet_id")
        wallet = get_object_or_404(Wallet.objects.select_related("user"), id=wallet_id)
        
        transactions = Transaction.objects.filter(wallet=wallet).select_related("membership").order_by("-created_at")
        
        form = TransactionFilterForm(self.request.GET or None)
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get("type"):
                transactions = transactions.filter(type=cd["type"])
            if cd.get("status"):
                transactions = transactions.filter(status=cd["status"])
            if cd.get("payment_method"):
                transactions = transactions.filter(payment_method=cd["payment_method"])
                
        memberships = Membership.objects.filter(user=wallet.user).order_by("-created_at")
        latest_membership = memberships.first()
        
        context.update({
			"wallet": wallet,
			"transactions": transactions[:50],
			"filter_form": form,
			"memberships": memberships,
			"latest_membership": latest_membership,
		})
        
        return context
