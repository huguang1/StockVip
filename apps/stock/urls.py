from django.urls import path

from .views import PersonalGainView
from .views import OfficialSharePriceView
from .views import TransactionHourView

app_name = "app_stock"

urlpatterns = [
    path('personal/', PersonalGainView.as_view(), name="personal"),
    path('official/', OfficialSharePriceView.as_view(), name="official"),
    path('transaction/', TransactionHourView.as_view(), name="transaction")
]