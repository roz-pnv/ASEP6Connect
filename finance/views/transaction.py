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
from finance.models.transaction import Transaction
from finance.models.transaction import TransactionType
from finance.models.transaction import TransactionStatus
from finance.models.transaction import PaymentMethod
from finance.forms.transaction import TransactionPurposeForm
from finance.forms.transaction import TransactionMethodForm
from finance.forms.transaction import VerificationForm


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transaction/transaction_detail.html"
    context_object_name = "transaction"
    pk_url_kwarg = "transaction_id"

    def get_queryset(self):
        return Transaction.objects.filter(wallet__user=self.request.user)


class UserTransactionPurposeView(LoginRequiredMixin, View):
    template_name = "transaction/user_create/transaction_step1.html"
    form_class = TransactionPurposeForm

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        action = request.GET.get("action")
        transaction_data = {}

        type_map = {
            "membership": TransactionType.MEMBERSHIP_FEE,
            "donate": TransactionType.DONATION,
            "deposit": TransactionType.DEPOSIT,
            "withdraw": TransactionType.WITHDRAWAL,
        }

        if action == "membership":
            last_tx = Transaction.objects.filter(
                wallet=wallet,
                type=TransactionType.MEMBERSHIP_FEE,
                status=TransactionStatus.PENDING
            ).order_by("-created_at").first()

            if last_tx:
                transaction_data = {
                    "type": last_tx.type,
                    "wallet_id": wallet.id,
                    "amount": last_tx.amount,
                    "membership_id": last_tx.membership_id,
                    "note": last_tx.note,
                    "tx_id": last_tx.id
                }
                request.session["transaction_data"] = transaction_data
                return redirect("user-transaction-method")

        elif action == "pay":
            tx_id = request.GET.get("tx_id")
            transaction = get_object_or_404(Transaction, id=tx_id, wallet=wallet)
            transaction_data = {
                "type": transaction.type,
                "wallet_id": wallet.id,
                "amount": transaction.amount,
                "note": transaction.note,
                "membership_id": transaction.membership_id,
                "tx_id": transaction.id
            }
            request.session["transaction_data"] = transaction_data
            return redirect("user-transaction-method")

        elif action in type_map:
            transaction_data = {
                "type": type_map[action],
                "wallet_id": wallet.id
            }
            request.session["transaction_data"] = transaction_data
            return redirect("user-transaction-method")

        transaction_data = request.session.get("transaction_data", {})
        transaction_type = transaction_data.get("type")
        initial_data = {
            "type": transaction_type,
            "note": transaction_data.get("note", "")
        }

        form = self.form_class(
            initial=initial_data,
            transaction_type=transaction_type,
            wallet=wallet
        )

        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet,
            "type": transaction_type
        })

    def post(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transaction_data = request.session.get("transaction_data", {})
        transaction_type = transaction_data.get("type")

        form = self.form_class(
            request.POST,
            initial={"type": transaction_type},
            transaction_type=transaction_type,
            wallet=wallet
        )

        if form.is_valid():
            transaction_data["note"] = form.cleaned_data.get("note", "")
            request.session["transaction_data"] = transaction_data
            return redirect("user-transaction-method")

        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet,
            "type": transaction_type
        })


class UserTransactionMethodView(LoginRequiredMixin, View):
    template_name = "transaction/user_create/transaction_step2.html"
    form_class = TransactionMethodForm

    def get(self, request):
        data = request.session.get("transaction_data", {})
        wallet = Wallet.objects.get(user=request.user)

        form = self.form_class(
            initial={
                "amount": data.get("amount"),
                "payment_method": data.get("payment_method"),
            },
            transaction_type=data.get("type"),
            wallet=wallet
        )

        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })

    def post(self, request):
        data = request.session.get("transaction_data", {})
        wallet = Wallet.objects.get(user=request.user)

        form = self.form_class(
            request.POST,
            initial={
                "amount": data.get("amount"),
                "payment_method": data.get("payment_method"),
            },
            transaction_type=data.get("type"),
            wallet=wallet
        )

        if form.is_valid():
            data.update({
                "payment_method": form.cleaned_data["payment_method"],
                "amount": form.cleaned_data["amount"]
            })

            request.session["transaction_data"] = data

            if data["payment_method"] == PaymentMethod.WALLET:
                return redirect("user-transaction-wallet-final")
            return redirect("user-transaction-code-request")

        return render(request, self.template_name, {
            "form": form,
            "wallet": wallet
        })


class UserTransactionWalletFinalizeView(LoginRequiredMixin, View):
    def get(self, request):
        data = request.session.get("transaction_data")
        wallet = request.user.wallet

        if wallet.balance < data["amount"]:
            messages.error(request, "Insufficient wallet balance.")
            return redirect("user-transaction-method")

        wallet.withdraw(data["amount"])
        transaction = Transaction.objects.create(
            wallet=wallet,
            type=data["type"],
            note=data.get("note", ""),
            amount=data["amount"],
            payment_method=PaymentMethod.WALLET,
            status=TransactionStatus.SUCCESS,
            membership_id=data.get("membership_id")
        )
        return redirect("user-transaction-confirmation", transaction_id=transaction.id)


class UserTransactionCodeRequestView(LoginRequiredMixin, View):
    template_name = "transaction/user_create/request_code.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.session.get("transaction_data")
        wallet = request.user.wallet

        tx_id = data.get("tx_id")
        if tx_id:
            transaction = get_object_or_404(Transaction, id=tx_id)
        else:
            transaction = Transaction.objects.create(
                wallet=wallet,
                type=data["type"],
                note=data.get("note", ""),
                amount=data["amount"],
                payment_method=PaymentMethod.ONLINE,
                status=TransactionStatus.PENDING,
                membership_id=data.get("membership_id")
            )

        request.session["transaction_id"] = transaction.pk
        verification_code = random.randint(100000, 999999)
        request.session["verification_code"] = verification_code

        send_mail(
            "Your Verification Code",
            f"Your verification code is: {verification_code}",
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False
        )

        return redirect("user-transaction-verify", transaction_id=transaction.pk)


class UserTransactionVerificationView(LoginRequiredMixin, View):
    template_name = "transaction/user_create/verify_code.html"
    form_class = VerificationForm

    def get(self, request, transaction_id):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        wallet = transaction.wallet
        form = self.form_class(request.POST)

        if form.is_valid():
            code = form.cleaned_data["code"]
            expected = request.session.get("verification_code")

            if str(code) == str(expected):
                wallet.deposit(transaction.amount)
                wallet.save()
                transaction.status = TransactionStatus.SUCCESS
            else:
                transaction.status = TransactionStatus.FAILED

            transaction.save()
            return redirect("user-transaction-confirmation", transaction_id=transaction.id)

        return render(request, self.template_name, {"form": form})


class UserTransactionConfirmationView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transaction/user_create/confirmation.html"
    context_object_name = "transaction"
    pk_url_kwarg = "transaction_id"