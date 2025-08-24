from django.utils import timezone
from django.db.models import Q

from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction
from finance.models.transaction import TransactionType
from finance.models.transaction import TransactionStatus

class WalletDetailView(LoginRequiredMixin, TemplateView):
    template_name = "wallet/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        wallet = Wallet.objects.filter(user=user).first()
        transactions = Transaction.objects.filter(
			wallet__user=user,
			status__in=[TransactionStatus.SUCCESS, TransactionStatus.FAILED]
		).order_by('-created_at')[:5]
				
        upcoming_tx_list = Transaction.objects.filter(
			wallet__user=user,  
			type=TransactionType.MEMBERSHIP_FEE,
			status__in=["pending", "failed"],
			created_at__gte=timezone.now() - timezone.timedelta(days=30),
		).filter(
			Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
		).order_by("created_at")
        
        context.update({
            "wallet": wallet,
            "transactions": transactions,
            "membership_url": "/membership/pay/",
            "donation_url": "/donate/",
            "transactions_url": "/finance/transactions/",
            "upcoming_tx_list": upcoming_tx_list,
        })

        return context
    
