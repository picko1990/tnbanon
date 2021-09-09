from django.db import models
from datetime import datetime
from main.utils.crypto import decrypt


class Operation(models.Model):

    AWAITING_RECEIPT = "awaiting_receipt"
    RECEIVED = "received"
    COMPENSATED = "compensated"
    SENT = "sent"

    STATUS_CHOICES = [
        (AWAITING_RECEIPT, "Awaiting Receipt"),
        (RECEIVED, "Received"),
        (COMPENSATED, "Compensated"),
        (SENT, "Sent")
    ]

    created_on = models.DateTimeField(auto_now_add=True)
    sending_date = models.DateTimeField(null=True)
    key = models.CharField(max_length=200)
    compensation_key = models.CharField(max_length=255)
    amount = models.IntegerField(null=True)
    total_amount = models.IntegerField(null=True)
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default=AWAITING_RECEIPT)
    sending_wallet_account_number = models.CharField(max_length=200)
    receiving_wallet_account_number = models.CharField(max_length=200)

    @property
    def minutes_left(self):
        time_left = self.sending_date.replace(tzinfo=None) - datetime.utcnow()
        return time_left.total_seconds() // 60

    @property
    def decrypted_compensation_key(self):
        return decrypt(self.compensation_key)

    def __str__(self):
        return f"{self.status}: {self.minutes_left}"
