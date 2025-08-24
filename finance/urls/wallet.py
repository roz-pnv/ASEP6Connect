from django.urls import path

from finance.views.wallet import WalletDetailView
from finance.views.transaction import TransactionDetailView

urlpatterns = [
    path('', WalletDetailView.as_view(), name='wallet-overview'),
	path("transaction/<int:transaction_id>/", TransactionDetailView.as_view(), name="transaction_detail"),
]
