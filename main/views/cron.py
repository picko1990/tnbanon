from django.views import View
from django.http import HttpResponse
from main.utils.wallets import send


class CronView(View):

    def get(self, request):
        send()
        return HttpResponse("just a cron")
