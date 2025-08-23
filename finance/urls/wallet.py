from django.urls import path
from finance.views.wallet import WalletDetailView

urlpatterns = [
    path('wallet/', WalletDetailView.as_view(), name='wallet-overview'),
]
