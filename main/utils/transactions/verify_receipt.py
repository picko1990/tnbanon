from main.models.receipt_log import ReceiptLog
from datetime import timedelta
from main.utils.transactions.get import get_transactions
from main.utils.confirmation_blocks import get_confirmation_blocks


def verify_receipt(amount, sender, recipient, period=timedelta(days=1)):
    transactions = get_transactions(period=period, recipient=recipient)

    for transaction in transactions:
        if (
            transaction["amount"] == amount
            and transaction["block"]["sender"] == sender
            and transaction["id"] not in [receipt_log.tx_id for receipt_log in ReceiptLog.objects.all()]
            # and transaction["block"]["id"] in [block["block"] for block in get_confirmation_blocks(period=period)]
        ):
            ReceiptLog.objects.create(tx_id=transaction["id"])
            return True

    return False
