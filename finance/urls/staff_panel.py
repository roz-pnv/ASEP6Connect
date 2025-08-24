from django.urls import path

from finance.views.staff_transaction import TransactionAdminView
from finance.views.staff_transaction import TransactionReceiptView
from finance.views.staff_transaction import ConfirmMembershipView
from finance.views.staff_transaction_create import TransactionPurposeView
from finance.views.staff_transaction_create import TransactionMethodView
from finance.views.staff_transaction_create import TransactionFinalizeView
from finance.views.staff_transaction_create import TransactionWalletFinalizeView
from finance.views.staff_transaction_create import TransactionCodeRequestView
from finance.views.staff_transaction_create import TransactionVerificationView
from finance.views.staff_transaction_create import TransactionConfirmationView
from finance.views.staff_wallet import WalletAdminView
from finance.views.staff_wallet import WalletDetailAdminView

urlpatterns = [
    path("transactions/", TransactionAdminView.as_view(), name="admin_transaction_list"),
	path("transactions/receipt/<int:transaction_id>/", TransactionReceiptView.as_view(), name="transaction_receipt"),
    path("transactions/create/<int:wallet_id>/", TransactionPurposeView.as_view(), name="transaction-purpose"),
    path("transactions/method/", TransactionMethodView.as_view(), name="transaction-method"),
    path("transactions/finalize/", TransactionFinalizeView.as_view(), name="transaction-finalize"),
    path("transactions/wallet/", TransactionWalletFinalizeView.as_view(), name="transaction-wallet-final"),
    path("transactions/online/initiate/", TransactionCodeRequestView.as_view(), name="transaction-online-initiate"),
    path("transactions/online/verify/<int:transaction_id>/", TransactionVerificationView.as_view(), name="transaction-online-verify"),
    path("transactions/online/confirm/<int:transaction_id>/", TransactionConfirmationView.as_view(), name="transaction-online-confirm"),

	path("wallet/", WalletAdminView.as_view(), name="admin_wallet_list"),
	path("wallet/<int:wallet_id>/", WalletDetailAdminView.as_view(), name="admin_wallet_detail"),

	path("memberships/confirm/<int:membership_id>/", ConfirmMembershipView.as_view(), name="confirm_membership"),
]
