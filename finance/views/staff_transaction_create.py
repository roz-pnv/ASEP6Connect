import uuid
import random

from django.utils import timezone
from datetime import timedelta
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction, TransactionStatus
from finance.models.transaction import PaymentMethod
from finance.models.transaction import TransactionStatus
from users.models.membership import Membership
from finance.forms.staff_transaction import (
    TransactionPurposeForm,
    TransactionMethodForm,
    TransactionExtraForm,
    VerificationForm
)


Users = get_user_model()

class TransactionPurposeView(LoginRequiredMixin, View):
    template_name = "transaction/staff_create/transaction_step1.html"
    form_class = TransactionPurposeForm

    def get_wallet(self, wallet_id):
        return get_object_or_404(Wallet, id=wallet_id)

    def get(self, request, wallet_id):
        form = self.form_class()
        wallet = self.get_wallet(wallet_id)
        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })

    def post(self, request, wallet_id):
        form = self.form_class(request.POST)
        wallet = self.get_wallet(wallet_id)
        if form.is_valid():
            request.session["transaction_data"] = {
                "type": form.cleaned_data["type"],
                "note": form.cleaned_data.get("note", ""),
                "wallet_id": wallet.id
            }
            return redirect("transaction-method")
        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })


class TransactionMethodView(LoginRequiredMixin, View):
    template_name = "transaction/staff_create/transaction_step2.html"
    form_class = TransactionMethodForm

    def get(self, request):
        data = request.session.get("transaction_data", {})
        wallet_id = data.get("wallet_id")
        wallet = get_object_or_404(Wallet, id=wallet_id)
        form = self.form_class(transaction_type=data.get("type"), wallet=wallet)
        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })

    def post(self, request):
        data = request.session.get("transaction_data", {})
        wallet_id = data.get("wallet_id")
        wallet = get_object_or_404(Wallet, id=wallet_id)

        form = self.form_class(request.POST, transaction_type=data.get("type"), wallet=wallet)
        if form.is_valid():
            data.update({
                "payment_method": form.cleaned_data["payment_method"],
                "amount": form.cleaned_data["amount"]
            })
            if "membership" in form.cleaned_data:
                data["membership_id"] = form.cleaned_data["membership"].id

            request.session["transaction_data"] = data

            method = form.cleaned_data["payment_method"]
            if method == PaymentMethod.WALLET:
                return redirect("transaction-wallet-final")
            elif method == PaymentMethod.ONLINE:
                return redirect("transaction-online-initiate")
            else:
                return redirect("transaction-finalize")

        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })


class TransactionWalletFinalizeView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.session.get("transaction_data")
        wallet_id = data.get("wallet_id")
        wallet = get_object_or_404(Wallet, id=wallet_id)

        if wallet.balance < data["amount"]:
            messages.error(request, "Insufficient wallet balance.")
            return redirect("transaction-method")

        wallet.withdraw(data["amount"])
        membership_id = data.get("membership_id")
        Transaction.objects.create(
            wallet=wallet,
            type=data["type"],
            note=data["note"],
            amount=data["amount"],
            payment_method=PaymentMethod.WALLET,
            status=TransactionStatus.SUCCESS,
            membership_id=membership_id if membership_id else None
        )
        messages.success(request, "Transaction completed using wallet.")
        return redirect("admin_wallet_detail", wallet_id=wallet.id)


class TransactionFinalizeView(LoginRequiredMixin, View):
    template_name = "transaction/staff_create/transaction_finalize.html"
    form_class = TransactionExtraForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = request.session.get("transaction_data")
            wallet_id = data.get("wallet_id")
            wallet = get_object_or_404(Wallet, id=wallet_id)

            membership_id = data.get("membership_id")
            Transaction.objects.create(
				wallet=wallet,
				type=data["type"],
				note=data["note"],
				amount=data["amount"],
				payment_method=data["payment_method"],
				related_project=form.cleaned_data.get("related_project"),
				status=TransactionStatus.SUCCESS,
				membership_id=membership_id if membership_id else None
			)
            messages.success(request, "Transaction recorded.")
            return redirect("admin_wallet_detail", wallet_id=wallet.id)
        return render(request, self.template_name, {"form": form})


class TransactionCodeRequestView(LoginRequiredMixin, View):
    template_name = 'transaction/staff_create/request_verification_code.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        transaction_data = request.session.get("transaction_data")
        if not transaction_data:
            messages.error(request, "Transaction data not found.")
            return redirect("transaction-method")

        wallet = get_object_or_404(Wallet, id=transaction_data["wallet_id"])

        # Create transaction object
        membership_id = transaction_data.get("membership_id")
        transaction = Transaction.objects.create(
			wallet=wallet,
			type=transaction_data["type"],
			note=transaction_data.get("note", ""),
			amount=transaction_data["amount"],
			payment_method=transaction_data["payment_method"],
			status=TransactionStatus.PENDING,
			membership_id=membership_id if membership_id else None
		)


        # Store transaction ID and verification code in session
        request.session["transaction_id"] = transaction.pk
        verification_code = random.randint(100000, 999999)
        request.session["verification_code"] = verification_code
    
        # Send via email
        send_mail(
            'Your Verification Code',
            f'Your verification code is: {verification_code}',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False
        )

        messages.success(request, "Verification code sent successfully.")
        return redirect(reverse("transaction-online-verify", kwargs={"transaction_id": transaction.pk}))


class TransactionVerificationView(LoginRequiredMixin, View):
    template_name = 'transaction/staff_create/verify_transaction_code.html'
    form_class = VerificationForm

    def get(self, request, transaction_id, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, transaction_id, *args, **kwargs):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        wallet = transaction.wallet
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data['verification_code']
            expected_code = request.session.get('verification_code')

            if str(expected_code) == str(code):
                wallet.balance += transaction.amount
                wallet.save()
                transaction.status = TransactionStatus.SUCCESS
                messages.success(request, "Transaction verified and completed.")
            else:
                transaction.status = TransactionStatus.FAILED
                messages.error(request, "Invalid verification code.")

            transaction.save()
            return redirect(reverse('transaction-online-confirm', kwargs={'transaction_id': transaction.pk}))

        return render(request, self.template_name, {'form': form})


class TransactionConfirmationView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transaction/staff_create/payment_confirm.html'
    context_object_name = 'transaction'
    pk_url_kwarg = 'transaction_id'


class CreatePendingTransactionView(LoginRequiredMixin, View):
    def post(self, request, wallet_id):
        wallet = get_object_or_404(Wallet, id=wallet_id)
        latest_membership = Membership.objects.filter(user=wallet.user).order_by('-created_at').first()

        if latest_membership and not latest_membership.is_confirmed:
            amount = latest_membership.required_payment
            expires_at = timezone.now() + timedelta(days=90)

            Transaction.objects.create(
                wallet=wallet,
                membership=latest_membership,
                type='membership_fee',
                amount=amount,
                status=TransactionStatus.PENDING,
                payment_method=PaymentMethod.ONLINE,
                expires_at=expires_at,
                note=(
                    "Dear member, your membership request is pending. "
                    "Please complete the payment of your annual membership fee "
                    f"({amount:,} Toman) within 3 months to activate your membership. "
                    "This transaction was initiated by the treasurer."
                )
            )

            messages.success(request, "Pending transaction created successfully.")
        else:
            messages.warning(request, "No pending membership found or already confirmed.")

        return redirect("admin_wallet_detail", wallet_id=wallet.id)
