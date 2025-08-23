import os
from django.db import models
from django.contrib.auth import get_user_model

from finance.models.wallet import Wallet
from users.models import Membership 

Users = get_user_model()


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class TransactionType(models.TextChoices):
    DEPOSIT = "deposit", "Deposit"
    WITHDRAWAL = "withdrawal", "Withdrawal"
    MEMBERSHIP_FEE = "membership_fee", "Membership Fee"
    DONATION = "donation", "Donation"


class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    CHEQUE = "cheque", "Cheque"
    ONLINE = "online", "Online Payment"
    WALLET = "wallet", "Wallet Balance"


class Transaction(models.Model):
    """
    Represents a financial transaction linked to a wallet.
    Includes deposits, withdrawals, membership fees, and donations.
    """
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions",
        help_text="Wallet this transaction belongs to"
    )
    membership = models.ForeignKey(
        Membership,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
        help_text="Related membership if this transaction is a membership fee"
    )
    note = models.TextField(
        blank=True,
        null=True,
        help_text="Optional note or description for the transaction"
    )
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        help_text="Current status of the transaction"
    )
    type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        help_text="Type of transaction (deposit, withdrawal, membership fee, donation)"
    )
    amount = models.BigIntegerField(
        help_text="Transaction amount in the smallest currency unit (e.g., cents)"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.ONLINE,
        help_text="Method used for this transaction (e.g., Cash, Cheque, Online Payment)"
    )   
    related_project = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Project name if this transaction is linked to a specific project"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the transaction was created"
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Deadline for completing this transaction"
    )

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["wallet", "created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        return f"{self.get_type_display()} of {self.amount} ({self.get_status_display()})"
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return self.status == TransactionStatus.PENDING and self.expires_at and timezone.now() > self.expires_at
    