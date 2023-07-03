from django.db import models

#
# class MemberManager(models.Manager):
#     def filter(self, **kwargs):
#         if 'user_name' in kwargs:
#             kwargs['user_name__iexact'] = kwargs['user_name']
#             del kwargs['user_name']
#         return super(MemberManager, self).filter(**kwargs)
#
#     def get(self, **kwargs):
#         if 'user_name' in kwargs:
#             kwargs['user_name__iexact'] = kwargs['user_name']
#             del kwargs['user_name']
#         return super(MemberManager, self).get(**kwargs)


# 会员帐号
class Member(models.Model):
    """
    user_name:会员帐号
    """
    user_name = models.CharField(max_length=128, null=False, unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

    # objects = MemberManager()

    class Meta:
        indexes = [
            models.Index(fields=["c_time"]),
            models.Index(fields=["user_name"])
        ]
        index_together = ["user_name", "c_time"]

        ordering = ['c_time']


# 会员资产
class MemberAssets(models.Model):
    """
    user: 关联会员账号ID
    category: 关联资产分类ID
    total_assets:总资产
    residual_assets:剩余资产
    buying_shares:买入股份
    selling_shares:卖出股份
    holding_shares:持有股份
    available_lottery:可用彩金
    c_time:创建时间
    """
    user = models.ForeignKey("Member", on_delete=models.CASCADE)
    category = models.ForeignKey("AssetsCategory", on_delete=models.CASCADE)
    total_assets = models.BigIntegerField(null=False)
    residual_assets = models.BigIntegerField(null=False)
    buying_shares = models.IntegerField(null=False, default=0)
    selling_shares = models.IntegerField(null=False, default=0)
    holding_shares = models.IntegerField(null=False, default=0)
    available_lottery = models.DecimalField(max_digits=16, decimal_places=2, null=False, default=0.00)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["c_time"])
        ]
        index_together = ["total_assets", "residual_assets", "buying_shares", "selling_shares",
                          "holding_shares", "available_lottery", "c_time"]

        ordering = ['-c_time']


# 资产分类
class AssetsCategory(models.Model):
    """
    name : 分类名称
    """
    name = models.CharField(max_length=128, null=False)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = ["name", "c_time"]
        ordering = ['id']


# 买入明细
class BuyDetails(models.Model):
    """
    user:用户名
    category:资产分类
    transaction_date:交易日期
    buying_shares:买入股份数量
    spend_coding:花费打码
    operating_time:操作时间
    """
    transaction_date = models.DateField(auto_now_add=True)
    buying_shares = models.IntegerField(null=False, default=0)
    spend_coding = models.BigIntegerField(null=False)
    operating_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("Member", on_delete=models.CASCADE)
    category = models.ForeignKey("AssetsCategory", on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=["operating_time"])]
        index_together = ["transaction_date", "buying_shares", "spend_coding", "operating_time"]
        ordering = ['-operating_time']


# 卖出明细
class SellDetails(models.Model):
    """
    user:用户名
    category:资产分类
    transaction_date:交易日期
    selling_shares:卖出股份
    official_price:官网股价
    personal_gain:个人股份增益
    earn_prize:获得彩金
    operating_time:操作时间, 创建时间
    """
    user = models.ForeignKey("Member", on_delete=models.CASCADE)
    category = models.ForeignKey("AssetsCategory", on_delete=models.CASCADE)
    transaction_date = models.DateField(auto_now_add=True)
    selling_shares = models.IntegerField(null=False, default=0)
    official_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    personal_gain = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    earn_prize = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    operating_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-operating_time']


# 彩金领取明细
class LotteryReceiptDetails(models.Model):
    """
    user:用户
    category:资产分类
    receive_bonus:领取彩金
    pickup_time:领取时间
    is_send:是否派彩
    send_time:派彩时间
    """
    user = models.ForeignKey("Member", on_delete=models.CASCADE)
    category = models.ForeignKey("AssetsCategory", on_delete=models.CASCADE)
    receive_bonus = models.DecimalField(max_digits=16, decimal_places=2, null=False, default=0.00)
    pickup_time = models.DateTimeField(auto_now_add=True)
    is_send = models.BooleanField(default=False)
    send_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-id']


# 在线会员
class OnlineMember(models.Model):
    """
    网站显示人数
    """
    people_count = models.BigIntegerField(null=False, default=800)
