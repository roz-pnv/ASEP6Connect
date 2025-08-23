from django.contrib import admin

from finance.models.wallet import Wallet
from finance.models.transaction import Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)
