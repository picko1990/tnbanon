from ..models.wallet import Wallet
from ..utils.crypto import encrypt
from ..utils.nacl_utils import get_account_number
from ..utils.accounts import create_account


def create_hybrid_a(hybrid_a):
    return Wallet.objects.create(
        signing_key=encrypt(hybrid_a),
        account_number=get_account_number(hybrid_a),
        label=Wallet.HYBRID_A
    )


def create_hybrid_b(hybrid_b):
    return Wallet.objects.create(
        signing_key=encrypt(hybrid_b),
        account_number=get_account_number(hybrid_b),
        label=Wallet.HYBRID_B
    )


def create_compensation_sender(compensation_sender):
    return Wallet.objects.create(
        signing_key=encrypt(compensation_sender),
        account_number=get_account_number(compensation_sender),
        label=Wallet.COMPENSATION_SENDER
    )


def create_compensation_receiver():
    signing_key, account_number = create_account()
    return Wallet.objects.create(
        signing_key=encrypt(signing_key),
        account_number=account_number,
        label=Wallet.COMPENSATION_RECEIVER
    )


def create_wallets(hybrid_a, hybrid_b, compensation_sender):
    Wallet.objects.all().delete()
    create_hybrid_a(hybrid_a)
    create_hybrid_b(hybrid_b)
    create_compensation_sender(compensation_sender)
    create_compensation_receiver()
