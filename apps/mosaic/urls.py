from django.urls import path
from .views import BuyDetailsView
from .views import SellDetailsView
from .views import MemberAssetsView
from .views import LotteryReceiptDetailsView
from .views import AssetsListView
from .views import AssetsOne
from .views import get_member_asset_csv
from .views import get_lottery_receipt_csv
from .views import OnlineMemberView
from .views import BuyDetailsListView
from .views import SellDetailsListView
from .views import LotteryReceiptDetailsListView
from .views import ExistDeliveryView

app_name = "app_mosaic"

urlpatterns = [
    path('buydtl/', BuyDetailsView.as_view(), name="bydtl"),
    path('selldtl/', SellDetailsView.as_view(), name="selldtl"),
    path('assets/', MemberAssetsView.as_view(), name="assets"),
    path('receiptdtl/', LotteryReceiptDetailsView.as_view(), name="receiptdtl"),
    path('assetslist/', AssetsListView.as_view(), name="assetslist"),
    path('assetsone/', AssetsOne.as_view(), name='assetsone'),
    path('memberassetcsv/', get_member_asset_csv, name="memberassetcsv"),
    path('lotteryreceiptcsv/', get_lottery_receipt_csv, name='lotteryreceiptcsv'),
    path('count/', OnlineMemberView.as_view(), name="count"),
    path('buydtllist/', BuyDetailsListView.as_view(), name="buydtllist"),
    path('selldtllist/', SellDetailsListView.as_view(), name="selldtllist"),
    path('receiptdtllist/', LotteryReceiptDetailsListView.as_view(), name="receiptdtllist"),
    path('exist/', ExistDeliveryView.as_view(), name='exist')
]