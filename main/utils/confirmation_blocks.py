import requests
from datetime import datetime, timedelta
from ..config import BANK_ADDRESS


def get_confirmation_block_time(block):
    block_time = block["created_date"].split("Z")[0]
    block_time = datetime.strptime(block_time, "%Y-%m-%dT%H:%M:%S.%f")
    return block_time


def get_confirmation_blocks(period=timedelta(days=1)):
    bank_address = BANK_ADDRESS
    response = requests.get(f"{bank_address}/confirmation_blocks?ordering=-created_date&limit=100").json()
    blocks = response["results"]

    if blocks:
        last_block_time = get_confirmation_block_time(block=blocks[-1])

        while response["next"] and datetime.utcnow() - last_block_time < period:
            response = requests.get(response["next"]).json()
            blocks.extend(response["results"])
            last_block_time = get_confirmation_block_time(block=blocks[-1])

        while datetime.utcnow() - last_block_time > period:
            blocks.pop()
            if blocks:
                last_block_time = get_confirmation_block_time(block=blocks[-1])
            else:
                break
    return blocks
