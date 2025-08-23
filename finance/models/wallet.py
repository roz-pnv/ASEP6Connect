import os
from django.db import models
from django.contrib.auth import get_user_model

Users = get_user_model()


class Wallet(models.Model):
    """
    Represents a user's wallet holding their current account balance.
    Each user has exactly one wallet.
    """
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="wallet",
        help_text="The user account associated with this wallet"
    )
    balance = models.BigIntegerField(
        default=0,
        help_text="Current balance of the wallet in the smallest currency unit (e.g., cents)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the wallet was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the wallet was last updated"
    )

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["balance"]),
        ]

    def __str__(self):
        return f"Wallet of {self.user.username} (Balance: {self.balance})"

    def deposit(self, amount: int):
        """Increase wallet balance by the given amount."""
        if amount > 0:
            self.balance += amount
            self.save(update_fields=["balance", "updated_at"])

    def withdraw(self, amount: int) -> bool:
        """Decrease wallet balance if sufficient funds exist."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save(update_fields=["balance", "updated_at"])
            return True
        return False
