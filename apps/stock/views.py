import logging

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views.generic import View
from django.http import QueryDict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.conf import settings

from utils import restful
from utils.add_logs import add_log
from utils.pagination import get_pagination_data

from .models import OfficialSharePrice
from .models import PersonalGain
from .models import TransactionHour
from .forms import TransactionHourForm
from .forms import PersonalGainForm
from .forms import OfficialSharePriceForm

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class PersonalGainView(View):
    """
    个人股价增益
    """
    
    def get(self, request):
        page = request.GET.get("p", 1)
        
        try:
            gains = PersonalGain.objects.all()
            paginator = Paginator(gains, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'gains': obj_page, 'count': len(gains)}
            context.update(context_data)
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_stock:personal"))
        else:
            return render(request, 'admin_tpl/stock/personal-gain.html', context=context)
    
    # 添加个人股票增益
    def post(self, request):
        # 表单验证
        form = PersonalGainForm(request.POST)
        
        # 表单验证成功
        if form.is_valid():
            # 获取表单中数据
            valid_bet = form.cleaned_data.get('valid_bet')
            grade_one = form.cleaned_data.get('grade_one')
            grade_two = form.cleaned_data.get('grade_two')
            grade_three = form.cleaned_data.get('grade_three')
            grade_four = form.cleaned_data.get('grade_four')
            grade_five = form.cleaned_data.get('grade_five')
            
            try:
                # 保存到数据库
                gain = PersonalGain(valid_bet=valid_bet, grade_one=grade_one, grade_two=grade_two,
                                    grade_three=grade_three, grade_four=grade_four, grade_five=grade_five)
                gain.save()
            except Exception as e:
                logger.error(e)  # 日志
                return restful.server_error(message="个人股价增益添加失败!")
            else:
                add_log("个人股价增益添加", "添加成功", request.user.username)
                return restful.ok()
        
        # 表单验证失败
        else:
            return restful.para_error(message=form.get_errors())
    
    # 更新个人股票增益
    def put(self, request):
        put_data = QueryDict(request.body)
        form = PersonalGainForm(put_data)
        if form.is_valid():
            valid_bet = form.cleaned_data.get('valid_bet')
            grade_one = form.cleaned_data.get('grade_one')
            grade_two = form.cleaned_data.get('grade_two')
            grade_three = form.cleaned_data.get('grade_three')
            grade_four = form.cleaned_data.get('grade_four')
            grade_five = form.cleaned_data.get('grade_five')
            gain_id = int(put_data.get('gain_id'))
            
            if gain_id:
                try:
                    gain = PersonalGain.objects.filter(pk=gain_id)
                    gain.update(valid_bet=valid_bet, grade_one=grade_one, grade_two=grade_two, grade_three=grade_three,
                                grade_four=grade_four, grade_five=grade_five)
                except Exception as e:
                    logger.error(e)
                    return restful.server_error(message="更新个人股票增益失败")
                else:
                    return restful.ok()
            else:
                return restful.para_error(message="更新个人股票增益失败")
        else:
            return restful.para_error(form.get_errors())
    
    # 删除个人股票增益
    def delete(self, request):
        del_data = QueryDict(request.body)
        gain_id = int(del_data.get('gain_id'))
        if gain_id:
            try:
                # 删除数据
                gain = PersonalGain.objects.get(pk=gain_id)
                gain.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除个人股票增益失败")
            else:
                add_log("删除个人股票增", "删除个人股票增成功", request.user.username)
                return restful.ok()
        else:
            return restful.server_error(message="删除个人股票增益失败")


@method_decorator(login_required, name='dispatch')
class OfficialSharePriceView(View):
    """
    官方股价
    """
    
    def get(self, request):
        page = request.GET.get("p", 1)
        
        try:
            prices = OfficialSharePrice.objects.all()
            paginator = Paginator(prices, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'prices': obj_page, 'count': len(prices)}
            context.update(context_data)
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_stock:official"))
        else:
            return render(request, 'admin_tpl/stock/official-share-price.html', context=context)
    
    # 添加报价
    def post(self, request):
        data = QueryDict(request.body)
        
        form = OfficialSharePriceForm(data)
        
        if form.is_valid():
            add_time = form.cleaned_data.get('add_time')
            price = form.cleaned_data.get('price')
            try:
                osp = OfficialSharePrice(add_time=add_time, price=price)
                osp.save()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="官方股价添加失败")
            else:
                # 添加成功,日期：2019-02-19,价格:5.55
                add_log('官网股价', "添加成功,日期：%s,价格:%s" % (add_time, price), request.user.username)
                return restful.ok()
        else:
            return restful.para_error(message=form.get_errors())
    
    # 删除报价
    def delete(self, request):
        data = QueryDict(request.body)
        price_id = int(data.get('price_id'))
        
        if id:
            try:
                OfficialSharePrice.objects.get(id=price_id).delete()
            except Exception as e:
                logger.error(e)  # 日志
                return restful.para_error(message="删除官方报价失败")
            else:
                # 添加成功,日期：2019-02-19,价格:5.55
                # add_log('官网股价', "添加成功,日期：2019-02-19,价格:5.55", request.user.username)
                add_log("官方股价", "删除成功,ID:%d" % price_id, request.user.username)
                return restful.ok()
        else:
            return restful.para_error(message="删除操作失败，请刷新数据重新操作!")
    
    # 编辑官方股价
    def put(self, request):
        data = QueryDict(request.body)
        price_id = int(data.get('price_id'))
        price = float(data.get('price'))
        
        if id and price:
            try:
                OfficialSharePrice.objects.filter(pk=price_id).update(price=price)
            except Exception as e:
                logger.error(e)  # 日志
                return restful.para_error("操作失败，请刷新数据重新操作!")
            else:
                add_log("官方股价", "编辑官方股价成功,ID:%d" % price_id, request.user.username)
                return restful.ok()
        else:
            return restful.para_error("操作失败，请刷新数据重新操作!")


@method_decorator(login_required, name='dispatch')
class TransactionHourView(View):
    """
    股市时间设置
    """
    
    def get(self, request):
        try:
            # 查询第一条数据
            date_objs = TransactionHour.objects.get(pk=1)
        except Exception as e:
            logger.error(e)
            # 避免数据库没有数据时模板报错,
            data = {
                "start_time": '',
                "end_time": '',
                "is_maintain": '',
                "maintain_desc": '',
                "start_a": '',
                "end_a": '',
                "close_desc": ''
            }
            return render(request, 'admin_tpl/stock/transaction-hour.html', context={'date': data})
        else:
            return render(request, 'admin_tpl/stock/transaction-hour.html', context={'date': date_objs})
    
    def post(self, request):
        """
        :param request:
        start_time:活动开始时间
        end_time:活动结束时间
        is_maintain:是否维护
        maintain_desc:维护提示
        start_a,end_a:日交易范围A
        start_b,end_b:日交易范围B
        close_desc:关闭提示
        :return:
        数据格式：{'code': code, 'message': message, 'data': data}
        code：状态码
        message：错误信息
        data：数据
        """
        # 表单验证
        form = TransactionHourForm(request.POST)
        
        # 表单验证通过
        if form.is_valid():
            # 获取表单数据
            start_time = form.cleaned_data.get("start_time")
            end_time = form.cleaned_data.get("end_time")
            is_maintain = form.cleaned_data.get("is_maintain")
            maintain_desc = form.cleaned_data.get("maintain_desc")
            start_a = form.cleaned_data.get("start_a")
            end_a = form.cleaned_data.get("end_a")
            # start_b = form.cleaned_data.get("start_b")
            # end_b = form.cleaned_data.get("end_b")
            close_desc = form.cleaned_data.get("close_desc")
            
            try:
                # 如果有数据,更新数据库
                hour = TransactionHour.objects.filter(pk=1)
                if hour.count():
                    hour.update(start_time=start_time, end_time=end_time, is_maintain=is_maintain,
                                maintain_desc=maintain_desc, start_a=start_a, end_a=end_a, close_desc=close_desc)
                # 如果没有，创建一条数据
                else:
                    hour = TransactionHour(start_time=start_time, end_time=end_time, is_maintain=is_maintain,
                                           maintain_desc=maintain_desc, start_a=start_a, end_a=end_a,
                                           close_desc=close_desc)
                    hour.save()
            except Exception as e:
                logger.error(e)  # 日志
                return restful.server_error(message="股市时间设置失败，请刷新数据重试!")
            else:
                return restful.ok()
        # 表单验证出错,返回错误信息
        else:
            return restful.para_error(form.get_errors())
