from django.shortcuts import render
from django.db.models import Q
from django.views.generic import View
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.utils.decorators import method_decorator

from utils import restful

from apps.mosaic.models import Member
from apps.mosaic.models import AssetsCategory
from apps.mosaic.models import MemberAssets

import logging

logger = logging.getLogger(__name__)


class IndexHandle(View):
    def get(self, request):
        categories = AssetsCategory.objects.all()
        try:
            del request.session["IS_SIGIN"]
        except KeyError:
            pass
        return render(request, 'index.html', context={"categories": categories})


# 登录
class LoginHandle(View):
    # 检查是否登录
    def get(self, request):
        user = request.session.get("IS_SIGIN", "")
        category_id = request.GET.get('category', '')
        
        if user and category_id:
            try:
                MemberAssets.objects.get(Q(user__user_name=user[0]) & Q(category__id=int(category_id)))
            except Exception as e:
                logger.error(e)
                return restful.result(data={'is_login': False})
            else:
                return restful.result(data={'is_login': True, 'username': user[0]})
        else:
            return restful.result(data={'is_login': False})
    
    # 登录
    def post(self, request):
        username = request.POST.get("username")
        category_id = request.POST.get('category', '')
        
        if username and category_id:
            try:
                MemberAssets.objects.get(Q(user__user_name=username) & Q(category__id=int(category_id)))
                user = Member.objects.get(user_name=username)
            except Exception as e:
                logger.error(e)
                return restful.para_error(message="用户没有资产")
            else:
                request.session["IS_SIGIN"] = [user.user_name, user.id]
                return restful.ok()
        else:
            return restful.para_error(message="用户不存在")


# 退出登录
def logout(request):
    try:
        del request.session["IS_SIGIN"]
    except KeyError:
        pass
    return restful.ok()
