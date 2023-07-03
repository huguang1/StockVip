from django.db import models


# 打码信息
class MemberInfo(models.Model):
    """
    category: 关联资产分类id
    username:会员帐号
    member_amount:打码金额
    member_date:打码日期
    is_update:是否更新
    """
    username = models.CharField(max_length=128, null=False)
    member_amount = models.BigIntegerField(default=0)
    member_date = models.DateField(null=False)
    is_update = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("mosaic.AssetsCategory", on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=["c_time"])
        ]
        index_together = ["username", "member_amount", "member_date", "is_update", "c_time"]
        ordering = ['-id']


# 打码更新
class MemberUpdate(models.Model):
    """
    category: 关联资产分类id
    member_date:打码日期
    is_member:是否更新
    """
    member_date = models.DateField(null=False)
    is_member = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey("mosaic.AssetsCategory", on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=["c_time"])
        ]
        index_together = ["member_date", "is_member", "c_time"]
        ordering = ['-c_time']
