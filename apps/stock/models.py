from django.db import models


# 个人股价增益 Personal gain
class PersonalGain(models.Model):
    """
    valid_bet:有效投注
    grade_one:真人视讯
    grade_two:电子游艺
    grade_three:体育赛事
    grade_four:彩票游戏
    grade_five:棋牌游戏
    c_time:创建时间
    U_time:更新时间
    """
    valid_bet = models.BigIntegerField(null=False, default=0)
    grade_one = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grade_two = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grade_three = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grade_four = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grade_five = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['valid_bet']


# 官方报价 Official share price
class OfficialSharePrice(models.Model):
    """
    add_time:股价日期
    price:官方股价
    c_time:创建时间
    U_time:更新时间
    """
    add_time = models.DateField()
    price = models.DecimalField(max_digits=16, decimal_places=2, null=False, default=0.00)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']


#  股市时间 transaction hour
class TransactionHour(models.Model):
    """
    start_time:活动开始时间
    end_time:活动结束时间
    is_maintain:是否维护
    maintain_desc:维护提示
    start_a,end_a:日交易范围A
    start_b,end_b:日交易范围B
    close_desc:关闭提示
    c_time:创建时间
    U_time:更新时间
    """
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    close_desc = models.CharField(max_length=255)
    is_maintain = models.BooleanField(default=False)
    maintain_desc = models.CharField(max_length=255, default="")
    start_a = models.TimeField()
    end_a = models.TimeField()
    # start_b = models.TimeField()
    # end_b = models.TimeField()
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
