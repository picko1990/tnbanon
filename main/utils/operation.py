import uuid
from django.db.models import Q
from ..models.wallet import Wallet
from ..config import MAX_AMOUNT_COEFFICIENT
from .amount import suggest_amount, get_minimum_possible_amount
from main.utils.transactions.get import get_transactions_by_amount
from .transactions.time import get_average_passed_time_in_minutes


def operation_possible_and_context(amount):
    context = {
        "amount": amount,
        "operation_possible": False,
    }

    query = Q(label=Wallet.HYBRID_A) | Q(label=Wallet.HYBRID_B)
    max_balance = max([wallet.actual_balance for wallet in Wallet.objects.filter(query)])
    if max_balance >= amount + 2:
        transactions = get_transactions_by_amount(amount, amount * MAX_AMOUNT_COEFFICIENT)[:5]
        if len(transactions) == 5:
            context = {
                "amount": amount,
                "operation_possible": True,
                "minimum_amount": get_minimum_possible_amount(amount),
                "maximum_amount": amount * MAX_AMOUNT_COEFFICIENT,
                "suggested_amount": suggest_amount(amount),
                "minimum_delay": 0,
                "maximum_delay": 1440,
                "suggested_delay": get_average_passed_time_in_minutes(transactions),
                "key": str(uuid.uuid4()),
            }

    return context
