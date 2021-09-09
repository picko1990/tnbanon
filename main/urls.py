from django.urls import path
from .views import test, enter_amount, status, created, setup, cron

urlpatterns = [
    path("", enter_amount.EnterAmountView.as_view(), name="enter_amount"),
    path("status/", status.StatusView.as_view(), name="status"),
    path("created/", created.CreatedView.as_view(), name="created"),
    path("setup/", setup.SetupView.as_view(), name="setup"),
    path("cron/", cron.CronView.as_view(), name="cron"),
    path("test/", test.TestView.as_view(), name="test"),
]
