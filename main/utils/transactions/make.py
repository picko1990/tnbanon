import requests
from main.utils.blocks import generate_block
from main.utils.banks import get_bank_config
from main.utils.accounts import get_balance_lock
from main.utils.nacl_utils import string_to_signing_key, get_account_number
from main.config import BANK_ADDRESS


def make_transaction(signing_key, recipient, amount, memo=None):
    bank_address = BANK_ADDRESS
    account_number = get_account_number(signing_key)
    signing_key = string_to_signing_key(signing_key)
    bank_config = get_bank_config()
    balance_lock = get_balance_lock(account_number, bank_config)
    transactions = [
        {
            'amount': amount,
            'recipient': recipient,
        },
        {
            'amount': bank_config['default_transaction_fee'],
            'fee': 'BANK',
            'recipient': bank_config['account_number'],
        },
        {
            'amount': bank_config['primary_validator']['default_transaction_fee'],
            'fee': 'PRIMARY_VALIDATOR',
            'recipient': bank_config['primary_validator']['account_number'],
        }
    ]
    transactions[0].update({'memo': memo} if memo else {})
    block = generate_block(account_number, balance_lock, signing_key, transactions)
    response = requests.post(f'{bank_address}/blocks', headers={'Content-Type': 'application/json'}, data=block)
    if response.status_code == 201:
        return True
    return False
