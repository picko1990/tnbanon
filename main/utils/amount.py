from ..config import MIN_AMOUNT_COEFFICIENT, MAX_AMOUNT_COEFFICIENT
from random import randint
import math


def get_minimum_possible_amount(amount):
    return math.ceil(amount / 100) * 100


def round_to_nearest_hundred(amount):
    return round(amount / 100) * 100


def suggest_amount(amount):
    suggested_amount = randint(int(MIN_AMOUNT_COEFFICIENT*100), int(MAX_AMOUNT_COEFFICIENT*100)) / 100 * amount
    suggested_amount = round_to_nearest_hundred(suggested_amount)

    return suggested_amount if suggested_amount >= get_minimum_possible_amount(amount) else suggested_amount + 100
