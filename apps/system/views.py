import logging

# django
from django.shortcuts import (render, redirect)
from django.urls import reverse
from django.views.decorators.http import (require_GET, require_POST)
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import (login, logout, authenticate)

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.conf import settings
from django.http import QueryDict
from django.core.cache import cache

# 自定义库
from utils import restful
from utils.captcha.captcha import captcha
from utils.get_real_ip import get_ip_addr
from utils.add_logs import add_log
from utils.pagination import get_pagination_data
from utils.system_info import get_system_info

# app
from .models import (User, Logs)
from .forms import (LoginForm, ChangAllPwdForm, ChangPwdForm, RegisterForm)
from apps.mosaic.models import (BuyDetails, SellDetails, LotteryReceiptDetails)

logger = logging.getLogger(__name__)

"""
# 打印sql语句
from django.db import connection
for sql in connection.queries:
    print(sql)
"""


@method_decorator(login_required, name='dispatch')
class Index(View):

    def get(self, request):
        data = get_system_info(request)
        data.update({'last_ip': request.user.last_login_ip, 'last_date': request.user.last_login})
        return render(request, 'admin_tpl/index.html', context=data)


@require_GET
def img_captcha(request):
    """
    验证码图片
    """
    pre_code_id = request.GET.get("p")
    cur_code_id = request.GET.get("c")

    if pre_code_id:
        cache.delete(pre_code_id)

    # 生成验证码
    name, text, img = captcha.generate_captcha()
    # 存入缓存中
    cache.set(cur_code_id, text.lower(), 5 * 60)
    # request.session[cur_code_id] = text.lower()
    # 返回图片
    return HttpResponse(img, content_type='image/jpg')


class Login(View):
    """
    登录
    """

    def get(self, request):
        return render(request, 'admin_tpl/system/login.html')

    def post(self, request):
        # 表单验证
        form = LoginForm(request.POST)
        if form.is_valid():
            # 获取表单中数据
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            img_captcha = form.cleaned_data.get('img_captcha')
            img_code_id = form.cleaned_data.get('img_code_id')

            # 验证码校验
            input_captcha = img_captcha.lower()
            # server_captcha = request.session.get(img_code_id, default=None)
            server_captcha = cache.get(img_code_id)

            if input_captcha == server_captcha:
                # 用户验证
                user = authenticate(request, username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        request.session.set_expiry(0)
                        ip = get_ip_addr(request)
                        try:
                            # 更新用户登录时间和登录ip
                            User.objects.filter(pk=user.pk).update(last_login_ip=user.now_ip, now_ip=ip)
                            # 添加操作日志
                            add_log("用户登录", '登录成功,IP地址:' + ip, user.username)
                        except Exception as e:
                            logger.error(e)  # 日志

                        return restful.ok()

                    else:
                        return restful.unauth('账户被冻结')

                else:
                    return restful.para_error('用户名或密码错误')

            else:
                return restful.para_error("验证码错误")

        else:
            #  获取表单错误信息
            errors = form.get_errors()
            return restful.para_error(message=errors)


@require_GET
@login_required
def logout_view(request):
    """
    退出登陆
    """
    # 退出登录
    add_log("用户登出", "用户登出成功", request.user.username)
    logout(request)
    # 跳转到登录页面
    return redirect(reverse('app_system:login'))


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    """
    修改当前登录用户密码
    """

    def get(self, request):
        return render(request, 'admin_tpl/system/modpwd.html')

    def post(self, request):
        form = ChangPwdForm(request.POST)

        if form.is_valid():
            oldpwd = form.cleaned_data.get('oldpwd')
            username = request.user.username
            user = authenticate(username=username, password=oldpwd)

            if user:
                newpwd = form.cleaned_data.get("newpwd1")
                user.set_password(newpwd)
                user.save()
                add_log("修改登录密码", "修改密码：用户名：" + username, username)
                return restful.ok()
            else:
                return restful.para_error(message="请输入正确的原密码")

        else:
            errors = form.get_errors()
            return restful.para_error(message=errors)


@method_decorator(login_required, name='dispatch')
class SystemUser(View):
    """
    用户管理
    """

    def get(self, request):
        page = int(request.GET.get('p', 1))

        try:
            # 查询所有用户
            users = User.objects.exclude(id=request.user.id)
            paginator = Paginator(users, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'users': obj_page, 'count': len(users)}
            context.update(context_data)
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_system:sysuser"))
        else:
            # context: users:所以用户的用户信息, conunt:用户数量
            return render(request, 'admin_tpl/system/sysuser.html', context=context)

    # 创建用户
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pwd1')
            user_type = form.cleaned_data.get('user_type')
            desc = form.cleaned_data.get("desc")
            activation = form.cleaned_data.get("activation")
            kwargs = {'is_active': True if activation == 1 else False, 'user_desc': desc}

            if user_type == 1:
                User.objects.create_superuser(username=username, password=password, **kwargs)
                return restful.ok()
            else:
                User.objects.create_user(username=username, password=password, **kwargs)
                return restful.ok()
        else:
            return restful.para_error(message=form.get_errors())

    # 编辑用户
    def put(self, request):
        data = QueryDict(request.body)
        user_id = int(data.get('user_id', 0))
        desc = data.get('desc')
        user_type = int(data.get('user_type', -1))
        activation = int(data.get('activation', -1))
        utype = False
        active = False

        if user_type == 1:
            utype = True
        else:
            utype = False

        if activation == 1:
            active = True
        else:
            active = False

        if user_id:
            if request.user.is_superuser:
                try:
                    user = User.objects.get(id=user_id)
                    user.is_superuser = utype
                    user.is_active = active
                    user.user_desc = desc
                    user.save()
                except Exception as e:
                    logger.error(e)
                    return restful.server_error(message="编辑失败,请刷新数据重试")
                else:
                    return restful.ok()
            else:
                return restful.unauth(message="没有权限编辑用户")

        else:
            return restful.para_error(message="编辑失败,请刷新数据重试")

    # 删除用户
    def delete(self, request):
        data = QueryDict(request.body)

        user_id = int(data.get('user_id', 0))

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                if request.user.is_superuser:
                    user.delete()
                else:
                    return restful.unauth(message="没有权限删除用户")
            except Exception as e:
                logger.error(e)
                return restful.para_error(message="用户不存在")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="删除用户失败, 请刷新数据后重试")


# 修改用户密码
@require_POST
@login_required
def chang_all_pwd(request):
    form = ChangAllPwdForm(request.POST)

    if form.is_valid():
        user_id = form.cleaned_data.get('user_id')

        if user_id:
            user_id = int(user_id)
            newpwd = form.cleaned_data.get("newpwd1")

            try:
                user = User.objects.get(id=user_id)
                if request.user.is_superuser:
                    user.set_password(newpwd)
                    user.save()
                    username = user.username
                    add_log("修改登录密码", "修改密码：用户名：" + username, username)
                else:
                    return restful.unauth(message="没有权限修改用户密码")
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="用户不存在")
            else:
                return restful.ok()
        else:
            return restful.para_error(message="用户不存在")

    else:
        errors = form.get_errors()
        return restful.para_error(message=errors)


@method_decorator(login_required, name='dispatch')
class SystemLogs(View):
    """
    操作日志
    """

    def get(self, request):
        page = request.GET.get('p', 1)

        try:
            # 查询所有日志
            logs = Logs.objects.all()
            # 对logs进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
            paginator = Paginator(logs, settings.PAGE_COUNT)
            obj_page = paginator.page(page)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'logs': obj_page, 'count': len(logs)}
            context.update(context_data)
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse("app_system:syslog"))
        else:
            # context: logs:所以日志, conunt:日志数量
            return render(request, 'admin_tpl/system/syslog.html', context=context)

    def delete(self, request):
        try:
            Logs.objects.all().delete()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error("清空日志失败，请刷新重试")
