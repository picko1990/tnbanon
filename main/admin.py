from django.contrib import admin
from .models.operation import Operation
from .models.receipt_log import ReceiptLog
from .models.wallet import Wallet

admin.site.register(ReceiptLog)
admin.site.register(Wallet)
admin.site.register(Operation)
