from django.db import models
from ..utils.accounts import get_balance


class Wallet(models.Model):

    COMPENSATION_SENDER = "compensation_sender"
    COMPENSATION_RECEIVER = "compensation_receiver"
    HYBRID_A = "hybrid_a"
    HYBRID_B = "hybrid_b"

    LABEL_CHOICES = [
        (COMPENSATION_SENDER, 'Compensation Sender'),
        (COMPENSATION_RECEIVER, 'Compensation Receiver'),
        (HYBRID_A, 'Hybrid A'),
        (HYBRID_B, 'Hybrid B')
    ]

    signing_key = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    total_scheduled = models.IntegerField(default=0)
    label = models.CharField(max_length=50, choices=LABEL_CHOICES)

    @property
    def balance(self):
        return get_balance(self.account_number)

    @property
    def actual_balance(self):
        return self.balance - self.total_scheduled

    def __str__(self):
        balance = self.balance
        return f"{self.label}: {balance-self.total_scheduled} / {balance}"
