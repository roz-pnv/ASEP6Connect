from django.urls import path

from finance.views.transaction import UserTransactionWalletFinalizeView
from finance.views.transaction import UserTransactionMethodView
from finance.views.transaction import UserTransactionPurposeView
from finance.views.transaction import UserTransactionCodeRequestView
from finance.views.transaction import UserTransactionConfirmationView
from finance.views.transaction import UserTransactionVerificationView

urlpatterns = [
	path("start/", UserTransactionPurposeView.as_view(), name="user-transaction-purpose"),
    path("method/", UserTransactionMethodView.as_view(), name="user-transaction-method"),
    path("wallet/final/", UserTransactionWalletFinalizeView.as_view(), name="user-transaction-wallet-final"),
    path("code/request/", UserTransactionCodeRequestView.as_view(), name="user-transaction-code-request"),
    path("verify/<int:transaction_id>/", UserTransactionVerificationView.as_view(), name="user-transaction-verify"),
    path("confirm/<int:transaction_id>/", UserTransactionConfirmationView.as_view(), name="user-transaction-confirmation"),
]
