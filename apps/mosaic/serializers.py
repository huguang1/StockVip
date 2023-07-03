from rest_framework import serializers

from .models import AssetsCategory
from .models import Member
from .models import MemberAssets
from .models import BuyDetails
from .models import SellDetails
from .models import LotteryReceiptDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "user_name")


class AssetsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsCategory
        fields = ("id", "name")


class AssetsSerializer(serializers.ModelSerializer):
    category = AssetsCategorySerializer()
    user = UserSerializer()
    
    class Meta:
        model = MemberAssets
        fields = ("id", "user", "category", "total_assets", "residual_assets", "buying_shares", "selling_shares",
                  "holding_shares", "available_lottery")


class BuyDetailsSerializer(serializers.ModelSerializer):
    category = AssetsCategorySerializer()
    user = UserSerializer()
    
    class Meta:
        model = BuyDetails
        fields = ('id', 'category', 'user', 'transaction_date', 'buying_shares', 'spend_coding', 'operating_time')


class SellDetailsSerializer(serializers.ModelSerializer):
    category = AssetsCategorySerializer()
    user = UserSerializer()
    
    class Meta:
        model = SellDetails
        fields = ('id', 'user', 'category', 'transaction_date', 'selling_shares', 'official_price', 'personal_gain',
                  'earn_prize', 'operating_time')


class LotteryReceiptDetailsSerializer(serializers.ModelSerializer):
    category = AssetsCategorySerializer()
    user = UserSerializer()
    
    class Meta:
        model = LotteryReceiptDetails
        fields = ('id', 'user', 'category', 'receive_bonus', 'pickup_time', 'is_send', 'send_time')
