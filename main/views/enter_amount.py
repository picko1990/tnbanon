from django.views import View
from django.shortcuts import render
from ..utils.operation import operation_possible_and_context


class EnterAmountView(View):

    def get(self, request):
        return render(request, "main/enter_amount.html")

    def post(self, request):
        amount = int(request.POST.get("amount"))
        context = operation_possible_and_context(amount)
        return render(request, "main/enter_amount.html", context)
