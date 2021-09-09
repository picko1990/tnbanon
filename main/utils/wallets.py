from ..models.wallet import Wallet
from ..models.operation import Operation
from .accounts import create_account
from main.utils.transactions.make import make_transaction
from main.utils.crypto import encrypt, decrypt
from django.db.models import Q


def choose_sending_wallet(operation):
    query = Q(label=Wallet.HYBRID_A) | Q(label=Wallet.HYBRID_B)
    wallets = Wallet.objects.filter(query)
    wallets = wallets.exclude(account_number=operation.receiving_wallet_account_number)

    account_numbers = {}
    for wallet in wallets:
        account_numbers.update({
            wallet.account_number: wallet.actual_balance
        })
    account_number = max(account_numbers, key=account_numbers.get)
    return account_number


def choose_receiving_wallet(operation):
    query = Q(label=Wallet.HYBRID_A) | Q(label=Wallet.HYBRID_B) | Q(label=Wallet.COMPENSATION_SENDER)
    wallets = Wallet.objects.filter(query).order_by('label')
    c_r_wallet = Wallet.objects.get(label=Wallet.COMPENSATION_RECEIVER)
    c_s_wallet = wallets[0]
    compensation_amount = operation.total_amount - operation.amount

    if c_s_wallet.actual_balance < compensation_amount:
        return c_r_wallet.account_number

    account_numbers = {}
    for wallet in wallets:
        account_numbers.update({
            c_r_wallet.account_number if wallet.label == Wallet.COMPENSATION_SENDER else wallet.account_number:
                wallet.actual_balance
        })
    account_number = min(account_numbers, key=account_numbers.get)
    return account_number


def compensate(operation):
    def calculate_transaction_amount():
        compensation_amount = operation.total_amount - operation.amount
        amount = compensation_sender.balance - compensation_amount - 2
        return amount

    compensation_sender = Wallet.objects.get(label=Wallet.COMPENSATION_SENDER)
    new_signing_key, new_account_number = create_account()
    operation.compensation_key = encrypt(new_signing_key)

    compensated = make_transaction(
        signing_key=decrypt(compensation_sender.signing_key),
        recipient=new_account_number,
        amount=calculate_transaction_amount()
    )
    if compensated:
        compensation_sender.signing_key, operation.compensation_key =\
            operation.compensation_key, compensation_sender.signing_key
        compensation_sender.account_number = new_account_number
        operation.status = Operation.COMPENSATED
        operation.save()
        compensation_sender.save()
        return True
    return False


def send():
    operations = Operation.objects.filter(status=Operation.COMPENSATED)
    for operation in operations:
        if operation.minutes_left < 0:
            signing_key = Wallet.objects.get(account_number=operation.sending_wallet_account_number).signing_key
            sent = make_transaction(
                signing_key=decrypt(signing_key),
                recipient=operation.receiver,
                amount=operation.amount
            )
            if sent:
                operation.status = Operation.SENT
                operation.save()
                remove_scheduled_amount(operation)


# TODO implements for compensation_sender too
def add_scheduled_amount(operation):
    sending_wallet = Wallet.objects.get(account_number=operation.sending_wallet_account_number)
    sending_wallet.total_scheduled += operation.amount
    sending_wallet.save()


def remove_scheduled_amount(operation):
    sending_wallet = Wallet.objects.get(account_number=operation.sending_wallet_account_number)
    sending_wallet.total_scheduled -= operation.amount
    sending_wallet.save()


# TODO create a more dynamic network fee variable
def empty_compensation_receiver(operation):
    compensation_receiver = Wallet.objects.get(label=Wallet.COMPENSATION_RECEIVER)
    if operation.receiving_wallet_account_number == compensation_receiver.account_number:
        balance = compensation_receiver.balance
        if balance > 2:
            make_transaction(
                signing_key=decrypt(compensation_receiver.signing_key),
                recipient=Wallet.objects.get(label=Wallet.COMPENSATION_SENDER).account_number,
                amount=(balance - 2)
            )
