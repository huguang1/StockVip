from django import forms
from utils.forms import FormMixin

from .models import BuyDetails
from .models import Member
from .models import MemberAssets
from .models import SellDetails
from .models import LotteryReceiptDetails
from .models import AssetsCategory

'''
# user: 用户名
# category: 资产分类
# transaction_date: 交易日期
# buying_shares: 买入股份
# spend_coding: 花费打码
# operating_time: 操作时间
'''


class BuyDetailsForms(forms.Form, FormMixin):
    user = forms.CharField(max_length=128, required=False)
    category = forms.CharField(required=False)
    count = forms.CharField(required=False)


class SellDetailsForms(forms.Form, FormMixin):
    user = forms.CharField(max_length=128, required=False)
    category = forms.CharField(required=False)
    count = forms.CharField(required=False)


class LotteryReceiptDetailsForms(forms.Form, FormMixin):
    user = forms.CharField(max_length=128, required=False)
    category = forms.CharField(required=False)
