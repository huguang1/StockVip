# import datetime
import csv
import random
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from django.http import QueryDict
from django.utils import timezone
from django.http import StreamingHttpResponse
from django.core.cache import cache

from utils import restful
from utils.add_logs import add_log
from utils.pagination import get_pagination_json_data
from utils.pagination import get_page_context
from utils.decorators import index_login_check
from utils.decorators import time_limit
from utils.date_handle import str_to_datetime
from utils.date_handle import str_to_date
from utils.down_csv import Echo

from .models import BuyDetails
from .models import SellDetails
from .models import LotteryReceiptDetails
from .models import MemberAssets
from .models import AssetsCategory
from .models import OnlineMember
from .serializers import AssetsSerializer
from .serializers import BuyDetailsSerializer
from .serializers import SellDetailsSerializer
from .serializers import LotteryReceiptDetailsSerializer
from .forms import BuyDetailsForms
from .forms import SellDetailsForms
from .forms import LotteryReceiptDetailsForms
from .common import get_today_price
from .common import get_personal_gain
from .common import get_sell_count
from .common import conf_category

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class MemberAssetsView(View):
    """
    会员资产
    """

    def get(self, request):
        try:
            category = AssetsCategory.objects.all()
            if not category:
                conf_category()
                category = AssetsCategory.objects.all()

            category_assets = category[0]
            assets = MemberAssets.objects.select_related('category', 'user').filter(category=category_assets)
            context = {'count': len(assets), 'categries': category}
            context_data = get_page_context(obj=assets, page=1)
            context.update(context_data)
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_mosaic:assets"))
        else:
            return render(request, 'admin_tpl/mosaic/member-assets.html', context=context)

    def delete(self, request):
        data = QueryDict(request.body)
        category_id = data.get("category", 0)

        if category_id:
            try:
                assets = MemberAssets.objects.filter(category__id=category_id)
                assets.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除会员资产失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除会员资产失败, 请刷新数据重试")


# 会员资产导出
@login_required
@require_GET
def get_member_asset_csv(request):
    category_id = int(request.GET.get("category", 0))

    # 创建时区UTC+8:00
    tz_utc_8 = timezone(timedelta(hours=8))
    # 获取时区UTC+8:00的当前时间
    date_now = datetime.now(tz_utc_8)
    # 格式化成字符串，用作文件名, 避免文件名冲突
    filename = date_now.strftime("%Y%m%d%H%M%S") + '_' + ''.join(random.sample('0123456789', 5)) + '.csv'

    try:
        if category_id == 0:
            category = AssetsCategory.objects.all().first()
        else:
            category = AssetsCategory.objects.get(pk=category_id)
        assets = MemberAssets.objects.select_related('user', 'category').filter(category=category)

    except Exception as e:
        logger.error(e)
    else:
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        if assets:
            rows = [[asset.user.user_name, asset.category.name, asset.total_assets, asset.residual_assets] for asset in
                    assets]
            rows.append(["会员账号", "资产分类", "会员资产", "剩余资产"])

            response = StreamingHttpResponse((writer.writerow(row) for row in rows[::-1]), content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename="%s"' % filename
            return response
        else:
            response = StreamingHttpResponse(writer.writerow(["会员账号", "资产分类", "会员资产", "剩余资产"]), content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename="%s"' % filename
            return response


@method_decorator(login_required, name='dispatch')
class AssetsListView(View):
    def get(self, request):
        # 分类ID
        category_n = int(request.GET.get("category", 0))
        # page: 第几页, 默认第1页
        page = int(request.GET.get('p', 1))
        # username
        username = request.GET.get('username', '')

        try:
            if category_n:
                category = AssetsCategory.objects.get(id=category_n)
            else:
                return redirect(reverse("app_mosaic:assets"))

            if username:
                assets = MemberAssets.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(user__user_name=username))
            else:
                assets = MemberAssets.objects.select_related('category', 'user').filter(category=category)

            # 对assets进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
            paginator = Paginator(assets, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
            # 序列化
            serializer = AssetsSerializer(obj_page, many=True)
            # 序列化后的数据
            tmp_data = serializer.data
            context = {'data': tmp_data, 'count': len(assets)}
            context.update({'pages_parm': context_data})

        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_mosaic:assets"))
        else:
            return restful.result(data=context)


@method_decorator(index_login_check, name='get')
class AssetsOne(View):
    """
    获取会员资产接口
    """

    def get(self, request):
        username = request.GET.get('username')
        category = request.GET.get('category')

        if username and category:
            category = int(category)
            # 查询用户资产
            try:
                asset = MemberAssets.objects.select_related('user', 'category').get(
                    Q(user__user_name=username) & Q(category__id=category))
            except Exception as e:
                logger.error(e)
                return restful.result(message="用户没有资产")
            else:
                # 可卖出股票数量
                sell_count = get_sell_count(asset)

                # 官方报价
                today_price, yesterday_price = get_today_price()

                # 个股价增益
                personal_gain = get_personal_gain(asset)

                data = {
                    'username': asset.user.user_name,
                    'total_assets': asset.total_assets,
                    'residual_assets': asset.residual_assets,
                    'buying_shares': asset.buying_shares,
                    'selling_shares': asset.selling_shares,
                    'holding_shares': asset.holding_shares,
                    'available_lottery': asset.available_lottery,
                    'today_price': today_price,
                    'yesterday_price': yesterday_price,
                    'personal_gain': personal_gain,
                    'sell_count': sell_count
                }

                # print(data, '2')

                return restful.result(data=data)
        else:
            return restful.para_error(message="用户不存在")


@method_decorator(index_login_check, name='post')
@method_decorator(time_limit, name='post')
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='delete')
class BuyDetailsView(View):
    """
    买入明细
    """

    def get(self, request):
        # 分类ID
        category_id = int(request.GET.get("category", 0))

        try:
            category = AssetsCategory.objects.all()
            if not category:
                conf_category()
                category = AssetsCategory.objects.all()
            if category_id:
                category_tmp = category.get(id=category_id)
            else:
                category_tmp = category[0]

            buy_details = BuyDetails.objects.select_related('category', 'user').filter(category=category_tmp)

            context = {'count': len(buy_details), 'categries': category}
            context_data = get_page_context(obj=buy_details, page=1)
            context.update(context_data)
        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:bydtl"))
        return render(request, 'admin_tpl/mosaic/buy-details.html', context=context)

    # 买入股票
    def post(self, request):
        forms = BuyDetailsForms(request.POST)
        if forms.is_valid():
            user = forms.cleaned_data.get('user')
            category = forms.cleaned_data.get('category')
            count = forms.cleaned_data.get('count')

            try:
                count = int(count)
                category = int(category)
                assets = MemberAssets.objects.prefetch_related('user', 'category').get(
                    Q(user__user_name=user) & Q(category__id=category))
                if ((assets.residual_assets / 10000) < count) or count <= 0:
                    return restful.para_error(message="交易失败, 请刷新数据重试")
                else:
                    buy = BuyDetails(user=assets.user, category=assets.category, buying_shares=count,
                                     spend_coding=count * 10000)
                    buy.save()
                    assets.residual_assets = assets.residual_assets - (count * 10000)
                    assets.buying_shares = assets.buying_shares + count
                    assets.holding_shares = assets.holding_shares + count
                    assets.save()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="交易失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="交易失败, 请刷新数据重试")

    # 删除所有买入明细
    def delete(self, request):
        data = QueryDict(request.body)
        category_id = int(data.get("category", 0))

        if category_id:
            try:
                buy_details = BuyDetails.objects.filter(category__id=category_id)
                buy_details.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除会员买入明细失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除会员买入明细失败, 请刷新数据重试")


@method_decorator(login_required, name='dispatch')
class BuyDetailsListView(View):
    def get(self, request):
        username = request.GET.get("user", '')
        category_id = int(request.GET.get("category", 0))
        date = request.GET.get("date", '')
        page = int(request.GET.get("p", 1))

        try:

            if category_id:
                category = AssetsCategory.objects.get(id=category_id)
            else:
                return redirect(reverse("app_mosaic:bydtl"))

            if username and not date:
                buy_details = BuyDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(user__user_name=username))
            elif not username and date:
                buy_details = BuyDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(transaction_date=str_to_date(date)))
            elif username and date:
                buy_details = BuyDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(transaction_date=str_to_date(date)) & Q(user__user_name=username))
            else:
                buy_details = BuyDetails.objects.select_related('category', 'user').filter(category=category)

            # 对buy_details进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
            paginator = Paginator(buy_details, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
            # 序列化
            serializer = BuyDetailsSerializer(obj_page, many=True)
            # 序列化后的数据
            tmp_data = serializer.data

            context = {'data': tmp_data, 'count': len(buy_details)}
            context.update({'pages_parm': context_data})
        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:bydtl"))
        else:
            return restful.result(data=context)


@method_decorator(index_login_check, name='post')
@method_decorator(time_limit, name='post')
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='delete')
class SellDetailsView(View):
    """
    卖出明细
    """

    def get(self, request):
        # 分类ID
        category_id = int(request.GET.get("category", 1))
        page = int(request.GET.get('p', 1))

        try:
            category = AssetsCategory.objects.all()
            if not category:
                conf_category()
                category = AssetsCategory.objects.all()

            sell_details = SellDetails.objects.select_related('category', 'user').filter(
                category=category.first())
            context = {'count': len(sell_details), 'categries': category}
            context_data = get_page_context(obj=sell_details, page=page)
            context.update(context_data)
        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:selldtl"))
        return render(request, 'admin_tpl/mosaic/sell-details.html', context=context)

    # 卖出股票
    def post(self, request):
        forms = SellDetailsForms(request.POST)
        if forms.is_valid():
            user = forms.cleaned_data.get('user')
            category = forms.cleaned_data.get('category')
            count = forms.cleaned_data.get('count')
            try:
                count = int(count)
                category = int(category)
                assets = MemberAssets.objects.prefetch_related('user', 'category').get(
                    Q(user__user_name=user) & Q(category__id=category))

                # 可卖出股票数量
                buying_count = get_sell_count(assets)

                # 官方报价
                today_price, yesterday_price = get_today_price()

                # 个股价增益
                personal_gain = get_personal_gain(assets)

                # 获得彩金 彩金 = (官网股价 + 个人股份增益) * 个人股份
                earn_prize = (today_price + personal_gain) * count

                if count > assets.holding_shares or count > buying_count or count > assets.buying_shares:
                    return restful.para_error(message="交易失败, 请刷新数据重试")
                else:
                    sell_details = SellDetails(user=assets.user, category=assets.category, selling_shares=count,
                                               official_price=today_price, personal_gain=personal_gain,
                                               earn_prize=earn_prize)

                    assets.holding_shares = assets.holding_shares - count
                    assets.selling_shares = assets.selling_shares + count
                    assets.available_lottery = assets.available_lottery + earn_prize

                    sell_details.save()
                    assets.save()

            except Exception as e:
                logger.error(e)
                return restful.server_error(message="交易失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="交易失败, 请刷新数据重试")

    # 删除所有卖出明细
    def delete(self, request):
        data = QueryDict(request.body)
        category_id = int(data.get("category", 0))

        if category_id:
            try:
                sell_details = SellDetails.objects.filter(category__id=category_id)
                sell_details.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除会员买入明细失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除会员买入明细失败, 请刷新数据重试")


@method_decorator(login_required, name='dispatch')
class SellDetailsListView(View):
    def get(self, request):
        username = request.GET.get("user", '')
        category_id = int(request.GET.get("category", 0))
        date = request.GET.get("date", '')
        page = int(request.GET.get("p", 1))

        try:
            if category_id:
                category = AssetsCategory.objects.get(id=category_id)
            else:
                return redirect(reverse("app_mosaic:selldtl"))

            if username and not date:
                sell_details = SellDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(user__user_name=username))
            elif not username and date:
                sell_details = SellDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(transaction_date=str_to_date(date)))
            elif username and date:
                sell_details = SellDetails.objects.select_related('category', 'user').filter(
                    Q(category=category) & Q(transaction_date=str_to_date(date)) & Q(user__user_name=username))
            else:
                sell_details = SellDetails.objects.select_related('category', 'user').filter(category=category)

            # 对buy_details进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
            paginator = Paginator(sell_details, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
            # 序列化
            serializer = SellDetailsSerializer(obj_page, many=True)
            # 序列化后的数据
            tmp_data = serializer.data
            context = {'data': tmp_data, 'count': len(sell_details)}
            context.update({'pages_parm': context_data})
        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:selldtl"))
        else:
            return restful.result(data=context)


@method_decorator(index_login_check, name='post')
@method_decorator(login_required, name='get')
@method_decorator(login_required, name='put')
@method_decorator(login_required, name='delete')
class LotteryReceiptDetailsView(View):
    """
    彩金领取明细
    """

    def get(self, request):
        # 分类ID
        category_id = int(request.GET.get("category", 1))
        page = int(request.GET.get('p', 1))

        try:
            category = AssetsCategory.objects.all()
            if not category:
                conf_category()
                category = AssetsCategory.objects.all()
            lottery_receipt_details = LotteryReceiptDetails.objects.select_related('category', 'user').filter(
                category__id=category_id)
            context = {'count': len(lottery_receipt_details), 'categries': category}
            context_data = get_page_context(obj=lottery_receipt_details, page=page)
            context.update(context_data)

        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:receiptdtl"))
        else:
            return render(request, 'admin_tpl/mosaic/lottery-receipt-details.html', context=context)

    # 领取彩金
    def post(self, request):
        forms = LotteryReceiptDetailsForms(request.POST)
        if forms.is_valid():
            user = forms.cleaned_data.get('user')
            category = forms.cleaned_data.get('category')
            try:
                category = int(category)
                assets = MemberAssets.objects.prefetch_related('user', 'category').get(
                    Q(user__user_name=user) & Q(category__id=category))

                if assets and (assets.available_lottery > 0):
                    lottery_receipt = LotteryReceiptDetails(user=assets.user, category=assets.category,
                                                            is_send=False,
                                                            receive_bonus=assets.available_lottery)
                    assets.selling_shares = 0
                    assets.available_lottery = 0

                    lottery_receipt.save()
                    assets.save()

                    cache.set(key="stock_update_receipt", value=True, timeout=None)
                else:
                    return restful.para_error(message="彩金不足")

            except Exception as e:
                logger.error(e)
                return restful.server_error(message="彩金领取失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message=forms.get_errors())

    # 标记派彩
    def put(self, request):
        data = QueryDict(request.body)
        receipt_id = int(data.get('receipt_id'), 0)
        if receipt_id:
            try:
                receipt = LotteryReceiptDetails.objects.get(id=receipt_id)
                receipt.is_send = True
                receipt.send_time = timezone.now()
                receipt.save()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="派彩失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="派彩失败, 请刷新数据重试")

    # 删除所有彩金领取明细
    def delete(self, request):
        data = QueryDict(request.body)
        category_id = int(data.get("category", 0))

        if category_id:
            try:
                lottery_receipt_details = LotteryReceiptDetails.objects.filter(category__id=category_id)
                lottery_receipt_details.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除会员彩金领取明细失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除会员彩金领取明细失败, 请刷新数据重试")


@method_decorator(login_required, name='dispatch')
class LotteryReceiptDetailsListView(View):
    def get(self, request):
        category_id = int(request.GET.get("category", 0))
        start_time = request.GET.get("start_time", '')
        end_time = request.GET.get("end_time", '')
        page = int(request.GET.get("p", 1))
        username = request.GET.get("user", '')

        try:
            if category_id:
                category = AssetsCategory.objects.get(id=category_id)
            else:
                return redirect(reverse("app_mosaic:receiptdtl"))

            if start_time and end_time:
                start_time = str_to_datetime(start_time)
                end_time = str_to_datetime(end_time)

                if username:
                    lottery_receipt_details = LotteryReceiptDetails.objects.filter(
                        Q(category=category) & Q(pickup_time__range=(start_time, end_time)) & Q(
                            user__user_name=username))
                else:
                    lottery_receipt_details = LotteryReceiptDetails.objects.filter(
                        Q(category=category) & Q(pickup_time__range=(start_time, end_time)))
            else:
                if username:
                    lottery_receipt_details = LotteryReceiptDetails.objects.filter(
                        Q(category=category) & Q(user__user_name=username))
                else:
                    lottery_receipt_details = LotteryReceiptDetails.objects.filter(Q(category=category))

            # 对lottery_receipt_details进行分页, 每页PAGE_COUNT条数据(PAGE_COUNT默认值: 15)
            paginator = Paginator(lottery_receipt_details, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
            # 序列化
            serializer = LotteryReceiptDetailsSerializer(obj_page, many=True)
            # 序列化后的数据
            tmp_data = serializer.data

            context = {'data': tmp_data, 'count': len(lottery_receipt_details)}
            context.update({'pages_parm': context_data})

        except Exception as e:
            logger.error(e)
            return redirect(reverse("app_mosaic:receiptdtl"))
        else:
            return restful.result(data=context)


# 导出彩金数据
@login_required
@require_GET
def get_lottery_receipt_csv(request):
    category_id = int(request.GET.get("category", 0))
    start_time = request.GET.get("start_time", '')
    end_time = request.GET.get("end_time", '')

    # 创建时区UTC+8:00
    tz_utc_8 = timezone(timedelta(hours=8))
    # 获取时区UTC+8:00的当前时间
    date_now = datetime.now(tz_utc_8)
    # 格式化成字符串，用作文件名, 避免文件名冲突
    filename = date_now.strftime("%Y%m%d%H%M%S") + '_' + ''.join(random.sample('0123456789', 5)) + '.csv'

    try:
        if category_id:
            category = AssetsCategory.objects.get(pk=category_id)
        else:
            category = AssetsCategory.objects.all().first()

        if start_time and end_time:
            start_time = str_to_datetime(start_time)
            end_time = str_to_datetime(end_time)
            details = LotteryReceiptDetails.objects.select_related('category', 'user').filter(
                Q(category=category) & Q(pickup_time__range=(start_time, end_time)))
        else:
            details = LotteryReceiptDetails.objects.select_related('category', 'user').filter(
                category=category)

    except Exception as e:
        logger.error(e)
    else:
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        if details:
            rows = [
                [detail.user.user_name, detail.category.name, detail.receive_bonus, detail.pickup_time,
                 '是' if detail.is_send else '否',
                 detail.send_time]
                for detail in details]
            rows.append(["会员账号", "彩金分类", "领取彩金", "领取时间", "是否派彩", "派彩时间"])

            response = StreamingHttpResponse((writer.writerow(row) for row in rows[::-1]), content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename="%s"' % filename
            return response
        else:
            response = StreamingHttpResponse(writer.writerow(["会员账号", "彩金分类", "领取彩金", "领取时间", "是否派彩", "派彩时间"]),
                                             content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename="%s"' % filename
            return response


class OnlineMemberView(View):
    """
    获取在线会员数量
    """

    def get(self, request):
        count = cache.get("online-count-stockvip")
        if not count:
            try:
                online_count = OnlineMember.objects.get(id=1)
                count = online_count.people_count
            except Exception as e:
                logger.error(e)
                count = 800
                OnlineMember.objects.create(people_count=count)

            cache.set(key="online-count-stockvip", value=count, timeout=None)

        return restful.result(data={'online_count': count})


class ExistDeliveryView(View):
    """
    是否有数据
    """

    def get(self, request):
        is_exist = cache.get('stock_update_receipt')
        cache.set(key="stock_update_receipt", value=False, timeout=None)
        return restful.result(data={"exist": is_exist})
