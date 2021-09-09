from datetime import datetime, timedelta


def get_transaction_time(transaction):
    transaction_time = transaction["block"]["created_date"].split("Z")[0]
    transaction_time = datetime.strptime(transaction_time, "%Y-%m-%dT%H:%M:%S.%f")
    return transaction_time


def get_average_passed_time(transactions):
    if transactions:
        now = datetime.utcnow()
        passed_times = [now - get_transaction_time(tx) for tx in transactions]
        return sum(passed_times, timedelta()) / len(transactions)
    return None


def get_average_passed_time_in_minutes(transactions):
    if transactions:
        now = datetime.utcnow()
        passed_times = [now - get_transaction_time(tx) for tx in transactions]
        average_passed_time = sum(passed_times, timedelta()) / len(transactions)
        return average_passed_time.total_seconds() // 60
    return None
