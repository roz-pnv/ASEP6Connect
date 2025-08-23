from django.urls import path

from finance.views.staff_transaction import TransactionAdminView
from finance.views.staff_wallet import WalletAdminView

urlpatterns = [
    path("transactions/", TransactionAdminView.as_view(), name="admin_transaction_list"),
	path("wallets/", WalletAdminView.as_view(), name="admin_wallet_list"),
]
