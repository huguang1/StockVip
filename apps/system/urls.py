from django.urls import path

from .views import logout_view
from .views import img_captcha
from .views import Index
from .views import Login
from .views import ChangePassword
from .views import chang_all_pwd
from .views import SystemUser
from .views import SystemLogs


app_name = "app_system"

urlpatterns = [
    path('login/', Login.as_view(), name="login"),
    path('img_captcha/', img_captcha, name="img_captcha"),
    path('index/', Index.as_view(), name='index'),
    path('logout/', logout_view, name='logout'),
    path('changepwd/', ChangePassword.as_view(), name="changepwd"),
    path('syslog/', SystemLogs.as_view(), name="syslog"),
    path('sysuser/', SystemUser.as_view(), name="sysuser"),
    path('changeallpwd/', chang_all_pwd, name="changeallpwd")
]
