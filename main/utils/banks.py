import requests
from ..config import BANK_ADDRESS


def get_bank_config(bank_address=BANK_ADDRESS):
    return requests.get(f"{bank_address}/config").json()
