import datetime
from django.utils.timezone import get_current_timezone


# 字符串转日期
def str_to_date(str_date):
    year_str, mon_str, day_str = str_date.split('-')
    return datetime.date(int(year_str), int(mon_str), int(day_str))


# 字符串转时间
def str_to_datetime(str_datetime):
    # return datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    date_str, time_str = str_datetime.split(' ')
    year_str, mon_str, day_str = date_str.split('-')
    hour_str, minute_str, second_str = time_str.split(':')
    # 创建时区UTC+8:00
    # tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))
    result = datetime.datetime(year=int(year_str), month=int(mon_str), day=int(day_str), hour=int(hour_str),
                               minute=int(minute_str), second=int(second_str), tzinfo=get_current_timezone())
    return result


# 判断字符串
def isString(obj):
    try:
        obj.lower() + obj.title() + obj + ""
    except:
        return False
    else:
        return True


# 获取昨天日期
def get_yesterday(str_date):
    if isString(str_date):
        today = str_to_date(str_date)
    else:
        today = str_date
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday
