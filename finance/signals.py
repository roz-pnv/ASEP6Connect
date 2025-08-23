from django.db.models.signals import post_save
from django.dispatch import receiver
from finance.models.transaction import Transaction, TransactionStatus, TransactionType
from finance.models.wallet import Wallet


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, created, **kwargs):
    if not created or instance.status != TransactionStatus.SUCCESS:
        return

    wallet = instance.wallet
    if instance.type in [TransactionType.DEPOSIT, TransactionType.MEMBERSHIP_FEE, TransactionType.DONATION]:
        wallet.deposit(instance.amount)
    elif instance.type == TransactionType.WITHDRAWAL:
        wallet.withdraw(instance.amount)
