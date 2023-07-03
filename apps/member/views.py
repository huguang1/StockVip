# 系统
import os
import csv
import random
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging
from threading import Thread

# import traceback  # 异常处理
# # traceback.print_exc() # 打印发生异常的详细信息(行号...)

# django
from django.db import connection
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.conf import settings
from django.db.models import Q
from bulk_update.helper import bulk_update
from django.db import transaction
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import QueryDict
from django.http import StreamingHttpResponse

# 自定义
from utils import restful
from utils.excel_read import ExcelRead
from utils.add_logs import add_log
# from utils.pagination import get_pagination_data
from utils.date_handle import str_to_date
from utils.pagination import get_page_context
# from utils.pagination import get_page_json_context
from utils.pagination import get_pagination_json_data
from utils.down_csv import Echo

# app
from .models import MemberInfo
from .models import MemberUpdate
from apps.mosaic.models import AssetsCategory
from apps.mosaic.models import MemberAssets
from apps.mosaic.models import Member
from .forms import MemberInfoForms
from .serializers import MemberInfoSerializer

logger = logging.getLogger(__name__)


# 查询打码信息
@require_GET
@login_required
def member_info_query(request):
    username = request.GET.get('username')
    date = request.GET.get('date')

    if not username and not date:
        return redirect(reverse('app_member:info'))
    elif username and not date:
        return restful.ok()
    elif not username and date:
        return restful.ok()


@method_decorator(login_required, name='dispatch')
class MemberInfoView(View):
    """
    打码信息
    """

    def get(self, request):
        try:
            category = AssetsCategory.objects.all()
            infos = MemberInfo.objects.select_related('category').all()
            context = {'count': len(infos), 'categories': category}  # 总共有多少条数据
            context_data = get_page_context(obj=infos, page=1)  # 分页
            context.update(context_data)
        except ExcelRead as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_member:info"))
        else:
            return render(request, 'admin_tpl/member/membe-info.html', context=context)

    # 添加打码信息
    def post(self, request):
        forms = MemberInfoForms(request.POST)

        if forms.is_valid():
            category_id = forms.cleaned_data.get('category')
            username = forms.cleaned_data.get('username')
            amount = forms.cleaned_data.get('amount')
            add_date = forms.cleaned_data.get('add_date')

            category = AssetsCategory.objects.get(id=int(category_id))

            info = MemberInfo(username=username, member_amount=int(amount), member_date=add_date,
                              is_update=False, category=category)

            try:
                update = MemberUpdate.objects.get(Q(member_date=add_date) & Q(category=category))
                if update and update.is_member:
                    update.is_member = False
                    update.save()
            except Exception as e:
                logger.warning(e)
                update = MemberUpdate(member_date=add_date, is_member=False, category=category)
                update.save()

            try:
                info.save()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="添加失败, 请刷新数据重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="添加失败, 请刷新数据重试")


# 获取一页打码信息的 json数据
class MemberInfoList(View):
    def get(self, request):
        page = request.GET.get('p', 1)
        date = request.GET.get('date', '')
        username = request.GET.get('username', '')
        try:
            # infos = None
            if date and username:
                infos = MemberInfo.objects.select_related('category').filter(Q(member_date=date) & Q(username=username))
            elif username and not date:
                infos = MemberInfo.objects.select_related('category').filter(username=username)
            elif not username and date:
                infos = MemberInfo.objects.select_related('category').filter(member_date=date)
            else:
                infos = MemberInfo.objects.select_related('category').all()

            # 对infos进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
            paginator = Paginator(infos, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
            # 序列化
            serializer = MemberInfoSerializer(obj_page, many=True)
            # 序列化后的数据
            tmp_data = serializer.data
            context = {'data': tmp_data, 'count': len(infos)}
            context.update({'pages_parm': context_data})

        except ExcelRead as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_member:info"))
        else:
            return restful.result(data=context)


# 打码信息导出
@require_GET
@login_required
def get_member_info_csv(request):
    member_date = request.GET.get('date')

    if member_date:
        # 创建时区UTC+8:00
        tz_utc_8 = timezone(timedelta(hours=8))
        # 获取时区UTC+8:00的当前时间
        date_now = datetime.now(tz_utc_8)
        # 格式化成字符串，用作文件名, 避免文件名冲突
        filename = date_now.strftime("%Y%m%d%H%M%S") + '_' + ''.join(random.sample('0123456789', 5)) + '.csv'

        try:
            member_date = str_to_date(member_date)
            members = MemberInfo.objects.filter(member_date=member_date)

        except Exception as e:
            logger.error(e)
        else:

            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)

            if members:
                rows = [[member.member_date, member.username, member.member_amount] for member in members]
                rows.append(["投注日期", "会员账号", "投注金额"])

                response = StreamingHttpResponse((writer.writerow(row) for row in rows[::-1]), content_type="text/csv")
                response['Content-Disposition'] = 'attachment;filename="%s"' % filename
                return response
            else:
                response = StreamingHttpResponse(writer.writerow(["投注日期", "会员账号", "投注金额"]), content_type="text/csv")
                response['Content-Disposition'] = 'attachment;filename="%s"' % filename
                return response

    else:
        return restful.para_error(message="请选择日期")


@method_decorator(login_required, name='dispatch')
class MemberUpdateView(View):
    """
    打码更新
    """

    def get(self, request):
        # page: 第几页, 默认第1页
        page = int(request.GET.get('p', 1))
        try:
            updates = MemberUpdate.objects.select_related('category').all()
            context = {'count': len(updates)}  # 总共有多少条数据
            context_data = get_page_context(obj=updates, page=page)  # 分页
            context.update(context_data)
        except ExcelRead as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_member:update"))
        else:
            return render(request, 'admin_tpl/member/member-update.html',
                          context=context)

    def delete(self, request):
        data = QueryDict(request.body)
        update_id = data.get('update_id')
        date = data.get('date')
        update_category = data.get('update_category')

        if update_id and date and update_category:
            try:
                updates = MemberUpdate.objects.filter(
                    Q(category__id=int(update_category)) & Q(member_date=str_to_date(date)) & Q(id=int(update_id)))
                infos = MemberInfo.objects.filter(
                    Q(member_date=str_to_date(date)) & Q(category__id=int(update_category)))
                infos.delete()
                updates.delete()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="删除失败, 请重试!")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除失败, 请重试!")

    # 打码更新
    def post(self, request):
        update_id = int(request.POST.get('update_id'))
        member_date = str_to_date(request.POST.get('date'))
        if member_date and update_id:
            try:
                # 打码更新(用来判断是否更新)
                update_data = MemberUpdate.objects.get(Q(id=update_id) & Q(member_date=member_date))

                if not update_data.is_member:
                    # 查询所以资产,关联的用户和分类
                    assets = MemberAssets.objects.select_related('category', 'user').filter(
                        category=update_data.category)
                    # 查询要更新的数据(根据打码日期查询)
                    infos = MemberInfo.objects.select_related('category').filter(
                        Q(member_date=update_data.member_date) & Q(category=update_data.category) & Q(is_update=False))

                    if not infos:
                        return restful.ok()

                    users = Member.objects.all()
                    newest_users_dict = dict()  # 创建用户后的所有用户存到字典中

                    # 会员用户表中没有数据
                    if not users:
                        # 批量创建会员用户
                        create_users = [Member(user_name=info.username) for info in infos]

                        if create_users:
                            Member.objects.bulk_create(create_users)
                            newest_users = Member.objects.all()
                            newest_users_dict = {user.user_name: user for user in newest_users}
                    # 会议用户表中有数据
                    else:
                        tmp_users = {user.user_name: user for user in users}

                        # 批量创建会员用户
                        create_users = [Member(user_name=info.username) for info in infos if
                                        info.username not in tmp_users]

                        if not create_users:
                            newest_users_dict = tmp_users
                        else:
                            # 批量创建会员用户
                            if create_users:
                                Member.objects.bulk_create(create_users)
                                newest_users = Member.objects.all()
                                newest_users_dict = {user.user_name: user for user in newest_users}

                    # 会员资产表没有数据
                    if not assets and newest_users_dict:
                        create_assets = [
                            MemberAssets(user=newest_users_dict[info.username], category=update_data.category,
                                         total_assets=info.member_amount, residual_assets=info.member_amount) for info
                            in infos]
                        if create_assets:
                            MemberAssets.objects.bulk_create(create_assets)
                    # 会员资产有数据
                    else:
                        infos_dict = {info.username: info for info in infos}
                        assets_dict = {asset.user.user_name: asset for asset in assets}

                        # 批量创建资产
                        create_assets = [MemberAssets(user=newest_users_dict[key], category=update_data.category,
                                                      total_assets=value.member_amount,
                                                      residual_assets=value.member_amount) for
                                         key, value in infos_dict.items() if key not in assets_dict]

                        # 批量更新资产
                        create_assets_id = [assets_dict[key].id for key, value in infos_dict.items() if
                                            key in assets_dict]
                        update_assets = MemberAssets.objects.select_related('user', 'category').filter(
                            id__in=create_assets_id)

                        for update in update_assets:
                            data_tmp = infos_dict[update.user.user_name]
                            update.total_assets = update.total_assets + data_tmp.member_amount
                            update.residual_assets = update.residual_assets + data_tmp.member_amount

                        MemberAssets.objects.bulk_create(create_assets)
                        with transaction.atomic():
                            Thread(target=bulk_update, args=[update_assets]).start()
                            # bulk_update(update_assets)
                    for info in infos:
                        info.is_update = True
                    with transaction.atomic():
                        Thread(target=bulk_update, args=[infos]).start()
                        # bulk_update(infos)
                        update_data.is_member = True
                        update_data.save()
                else:
                    return restful.ok()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="更新失败,请重试")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="更新失败,请重试")


# 上传文件接口
@require_POST
@login_required
def upload_file(request):
    # 接收文件对象
    file = request.FILES.get('file')
    # 获取文件扩展名
    ex_name = file.name.split('.')[-1]
    if ex_name != 'xls' and ex_name != 'xlsx':
        return restful.para_error(message="必须是excel文件，后缀名为　.xls　或者　.xlsx")
    # 创建时区UTC+8:00
    tz_utc_8 = timezone(timedelta(hours=8))
    # 获取时区UTC+8:00的当前时间
    date_now = datetime.now(tz_utc_8)
    # 格式化成字符串，用作文件名
    name = date_now.strftime("%Y%m%d%H%M%S") + '.' + ex_name

    # 文件保存到指定目录
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    # 返回文件名称
    return restful.result(data={'name': name})


@method_decorator(login_required, name='dispatch')
class ImportDataView(View):
    """
    导入数据
    """

    def get(self, request):
        try:
            categories = AssetsCategory.objects.all()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="导入数据异常, 请重试")
        else:
            return render(request, 'admin_tpl/member/member-import.html', context={'categories': categories})

    # 数据导入到数据库
    def post(self, request):
        # 获取参数
        name = request.POST.get('filename')
        date = request.POST.get('ipt_time')
        category_id = int(request.POST.get('category', 0))

        if not name:
            return restful.para_error("文件无效,请重新上传")
        else:
            try:
                # 参数处理: 解析excel表格中的数据
                src_data = ExcelRead(os.path.join(settings.MEDIA_ROOT, name)).read_excel()
                if not src_data:
                    return restful.para_error(message="Excel表格没有数据数据")
            except Exception as e:
                logging.error(e)
                return restful.para_error(message="Excel表格数据格式并不正确,导入数据失败,请重新导入")

        # 参数校验
        if not date:
            return restful.para_error("请选择导入日期")
        if not category_id:
            return restful.para_error("请选择导入类型")
        if not src_data:
            return restful.para_error(message="用户名重复!")
        else:
            try:
                date = str_to_date(date)
                category = AssetsCategory.objects.get(pk=category_id)
                # 保存新建数据
                member_info_list = []
                for key, value in src_data.items():
                    member_info_list.append(
                        MemberInfo(username=key, member_amount=value, member_date=date, is_update=False,
                                   category=category))

                # 在事务中批量插入数据
                Thread(target=MemberInfo.objects.bulk_create, args=[member_info_list]).start()
                # run = Thread(target=MemberInfo.objects.bulk_create, args=[member_info_list])
                # run.start()
                # run.join()
            except Exception as e:
                logger.error(e)  # 日志
                return restful.para_error(message="导入数据失败,请重新导入")
            else:
                try:
                    update = MemberUpdate.objects.get(Q(member_date=date) & Q(category=category))
                    if update and update.is_member:
                        update.is_member = False
                        update.save()
                except Exception as e:
                    logger.warning(e)
                    update = MemberUpdate(member_date=date, is_member=False, category=category)
                    update.save()
                    add_log(name="导入数据", username=request.user.username, content="导入数据成功")
                else:
                    return restful.ok()
