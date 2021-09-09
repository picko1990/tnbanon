from django.views import View
from django.shortcuts import render
from ..utils.nacl_utils import string_to_signing_key
from ..utils.setup import create_wallets


class SetupView(View):

    def get(self, request):
        return render(request, "main/setup.html")

    def post(self, request):
        hybrid_a = request.POST.get("hybrid_a")
        hybrid_b = request.POST.get("hybrid_b")
        compensation_sender = request.POST.get("compensation_sender")
        try:
            string_to_signing_key(hybrid_a)
            string_to_signing_key(hybrid_b)
            string_to_signing_key(compensation_sender)
        except Exception:
            return render(request, "main/setup.html", {"message": "Invalid signing key entered"})

        keys = [hybrid_a, hybrid_b, compensation_sender]
        if len(keys) != len(set(keys)):
            return render(request, "main/setup.html", {"message": "Identical keys entered"})

        create_wallets(hybrid_a, hybrid_b, compensation_sender)
        context = {
            "message": "setup successful",
        }
        return render(request, "main/setup.html", context)
