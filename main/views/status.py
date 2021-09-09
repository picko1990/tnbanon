from django.views import View
from django.shortcuts import render
from ..models.operation import Operation
from main.utils.transactions.verify_receipt import verify_receipt
from ..utils.wallets import add_scheduled_amount, compensate, empty_compensation_receiver


class StatusView(View):

    def get(self, request):
        return render(request, "main/status.html")

    def post(self, request):
        key = request.POST.get("key")

        try:
            operation = Operation.objects.get(key=key)
        except Operation.DoesNotExist:
            context = {
                "message": "please enter a valid key"
            }
            return render(request, "main/status.html", context)

        if operation.status == Operation.AWAITING_RECEIPT:
            received = verify_receipt(
                operation.total_amount, operation.sender, operation.receiving_wallet_account_number
            )

            if received:
                operation.status = Operation.RECEIVED
                operation.save()
                add_scheduled_amount(operation)
                empty_compensation_receiver(operation)
                compensate(operation)

        context = {
            "operation": operation,
        }
        return render(request, "main/status.html", context)
