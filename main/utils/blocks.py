import json
from operator import itemgetter


def generate_block(account_number, balance_lock, signing_key, transactions):
    message = {
        'balance_key': balance_lock,
        'txs': sorted(transactions, key=itemgetter('recipient'))
    }
    signature = signing_key.sign(
        json.dumps(message, separators=(',', ':'), sort_keys=True).encode('utf-8')).signature.hex()
    block = {
        'account_number': account_number,
        'message': message,
        'signature': signature
    }
    return json.dumps(block)
