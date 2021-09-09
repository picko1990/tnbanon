import requests
from .nacl_utils import generate_signing_key, get_account_number
from .banks import get_bank_config


def create_account():
    signing_key = generate_signing_key()
    account_number = get_account_number(signing_key)
    return signing_key, account_number


def get_balance(account_number, bank_config=get_bank_config()):
    pv_protocol = bank_config["primary_validator"]["protocol"]
    pv_ip_address = bank_config["primary_validator"]["ip_address"]
    pv_port = bank_config["primary_validator"]["port"]
    pv_port = f":{pv_port}" if pv_port else ""
    url = f"{pv_protocol}://{pv_ip_address}{pv_port}/accounts/{account_number}/balance"
    balance = requests.get(url).json()["balance"]
    return balance or 0


def get_balance_lock(account_number, bank_config=get_bank_config()):
    pv_protocol = bank_config["primary_validator"]["protocol"]
    pv_ip_address = bank_config["primary_validator"]["ip_address"]
    pv_port = bank_config["primary_validator"]["port"]
    pv_port = f":{pv_port}" if pv_port else ""
    url = f"{pv_protocol}://{pv_ip_address}{pv_port}/accounts/{account_number}/balance_lock"
    return requests.get(url).json()["balance_lock"]
