from django.utils import timezone
from django.db.models import Q

from utils.date_handle import get_yesterday

from apps.stock.models import OfficialSharePrice
from apps.stock.models import PersonalGain
from .models import BuyDetails
from .models import AssetsCategory
from apps.member.models import MemberInfo

import logging

logger = logging.getLogger(__name__)


# 可卖出股票数量
def get_sell_count(asset):
    # 可卖出股票
    sell_count = 0
    # 今天日期
    today = timezone.now().date()
    # 获取昨日期
    yesterday = get_yesterday(today)
    
    try:
        buy = BuyDetails.objects.filter(Q(user=asset.user) & Q(category=asset.category))
    except Exception as e:
        logger.error(e)
        return sell_count
    else:
        # 可卖出股票数量
        if buy:
            
            tmp_count = 0
            for b in buy:
                tmp_count += b.buying_shares
                
                if b.transaction_date <= yesterday:
                    sell_count += b.buying_shares
                if tmp_count == (asset.buying_shares - asset.selling_shares):
                    break
        
        # buying_shares: 买入股份
        # selling_shares: 卖出股份
        # holding_shares: 持有股份
        # 买入数量 - 持有数量 = 卖出数量
        # 持有数量 = 买入数量 - 卖出数量
        
        sell_count = sell_count - (asset.buying_shares - asset.holding_shares)
        
        if sell_count < 0:
            buying_count = 0
            return buying_count
        else:
            return sell_count


# 个人股价增益
def get_personal_gain(asset):
    # 个人股价增益
    personal_gain = -2
    tmp_valid = 0
    try:
        # 查询个人股价增益
        gains = PersonalGain.objects.all()
        # 存到列表中
        valid = [gain.valid_bet for gain in gains]
    except Exception as e:
        logger.error(e)
        return personal_gain
    # 会员账号,用户名
    username = asset.user.user_name
    # 资产分类
    category = asset.category
    # 当前时间
    today = timezone.now().date()
    # 获取昨日期
    yesterday = get_yesterday(today)
    # 当天更新的资产
    residual = 0
    
    try:
        infos = MemberInfo.objects.filter(
            Q(username=username) & Q(member_date=yesterday) & Q(category=category) & Q(is_update=True))
    except Exception as e:
        logger.error(e)
        personal_gain = -2
        return personal_gain
    
    if infos:
        for info in infos:
            residual += info.member_amount
    else:
        personal_gain = -2
        return personal_gain
    
    if residual:
        for i in range(len(valid)):
            # 更新金额等于0
            if i == 0 and valid[i] >= residual and residual <= 0:
                tmp_valid = valid[i]
                break
            # 更新金额大于　50000000
            elif i == (len(valid) - 1) and residual >= valid[len(valid) - 1]:
                tmp_valid = valid[len(valid) - 1]
                break
            elif i != 0 and i != (len(valid) - 1) and (valid[i] <= residual) and (residual < valid[i + 1]):
                tmp_valid = valid[i]
                break
    else:
        personal_gain = -2
        return personal_gain
    
    for gain in gains:
        if gain.valid_bet == tmp_valid:
            personal_gain = gain.grade_one
            break
    
    return personal_gain


# 获取最新官方报价
def get_today_price():
    # 获取今天日期
    today = timezone.now().date()
    # 昨日时间
    yesterday = get_yesterday(today)
    
    # 今日报价
    today_price = 0
    # 昨日报价
    yesterday_price = 0
    try:
        prices = OfficialSharePrice.objects.all()
    except Exception as e:
        logger.error(e)
        today_price = 0
        yesterday_price = 0
    else:
        if prices:
            try:
                price = OfficialSharePrice.objects.get(add_time=today)
            except Exception as e:
                logger.error(e)
                if prices:
                    if len(prices) > 2:
                        prices_tmp = prices[:2]
                        today_price = prices_tmp[0].price
                        yesterday_price = prices_tmp[1].price
                    else:
                        today_price = prices.last().price
                        yesterday_price = 0
                else:
                    # 今日报价
                    today_price = 0
                    # 昨日报价
                    yesterday_price = 0
            else:
                today_price = price.price
                try:
                    y_price = OfficialSharePrice.objects.get(add_time=yesterday)
                except Exception as e:
                    logger.error(e)
                    yesterday_price = 0
                else:
                    yesterday_price = y_price.price
        else:
            today_price = 0
            yesterday_price = 0
    return today_price, yesterday_price


def conf_category():
    tmp = ["电子游艺", "视讯直播", "体育赛事", "彩票游戏", "棋牌游戏"]
    AssetsCategory.objects.bulk_create([AssetsCategory(name=name) for name in tmp])
