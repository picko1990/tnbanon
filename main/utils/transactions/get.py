import requests
from datetime import datetime, timedelta
from main.config import BANK_ADDRESS
from main.utils.transactions.time import get_transaction_time


def get_transactions(period=timedelta(days=1), recipient=""):
    bank_address = BANK_ADDRESS
    response = requests.get(
        f"{bank_address}/bank_transactions?ordering=-block__created_date&recipient={recipient}&limit=100"
    ).json()
    txs = response["results"]
    if txs:
        last_tx_time = get_transaction_time(transaction=txs[-1])

        while response["next"] and datetime.utcnow() - last_tx_time < period:
            response = requests.get(response["next"]).json()
            txs.extend(response["results"])
            last_tx_time = get_transaction_time(transaction=txs[-1])

        while datetime.utcnow() - last_tx_time > period:
            txs.pop()
            if txs:
                last_tx_time = get_transaction_time(transaction=txs[-1])
            else:
                break
    return txs


def get_transactions_by_amount(min_amount, max_amount=None, period=timedelta(days=1)):
    txs = get_transactions(period=period)

    if max_amount:
        return [tx for tx in txs if min_amount <= tx["amount"] <= max_amount]

    return [tx for tx in txs if min_amount <= tx["amount"]]
