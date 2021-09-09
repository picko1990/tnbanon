from django.db import models


class ReceiptLog(models.Model):
    tx_id = models.CharField(max_length=200)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tx_id
