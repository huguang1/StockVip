from rest_framework import serializers

from .models import MemberInfo

from apps.mosaic.serializers import AssetsCategorySerializer


class MemberInfoSerializer(serializers.ModelSerializer):
    category = AssetsCategorySerializer()

    class Meta:
        model = MemberInfo
        fields = ('id', 'username', 'member_amount', 'member_date', 'is_update', 'category')
