from django.shortcuts import render, redirect
from django.views import View
from datetime import timedelta, datetime
from ..utils.wallets import choose_receiving_wallet, choose_sending_wallet
from ..utils.nacl_utils import string_to_verify_key
from ..models.operation import Operation


class CreatedView(View):

    def get(self, request):
        return redirect("enter_amount")

    def post(self, request):
        sender = request.POST.get("sender")
        receiver = request.POST.get("receiver")
        try:
            string_to_verify_key(sender)
            string_to_verify_key(receiver)
        except Exception:
            return render(request, "main/enter_amount.html", {"error": "Invalid account number"})

        delay = int(request.POST.get("delay"))
        key = request.POST.get("key")
        operation, created = Operation.objects.get_or_create(key=key)
        if created:
            operation.sender = sender
            operation.receiver = receiver
            operation.amount = int(request.POST.get("amount"))
            operation.total_amount = int(request.POST.get("total_amount"))
            operation.sending_date = datetime.utcnow() + timedelta(minutes=delay)
            operation.receiving_wallet_account_number = choose_receiving_wallet(operation)
            operation.sending_wallet_account_number = choose_sending_wallet(operation)
            operation.save()
        context = {
            "operation": operation
        }

        return render(request, "main/created.html", context)
