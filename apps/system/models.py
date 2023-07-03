from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager


# 用户管理
class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')
        
        # if 'is_active' in kwargs:
        #     is_active = kwargs['is_active']
        # else:
        #     is_active = True
        #
        # if 'desc' in kwargs:
        #     user_desc = kwargs['desc']
        # else:
        #     user_desc = ''
        
        # print(kwargs)
        
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, username, password, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, **kwargs)
    
    def create_superuser(self, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)


# 管理员用户
class User(AbstractBaseUser, PermissionsMixin):
    """
    username:会员帐号
    user_desc:备注名称
    is_superuser管理类型
    is_active:状态
    last_login:上次登录时间
    last_login_ip:上次登录IP
    now_ip:当前登录IP
    u_time:更新时间
    """
    
    username = models.CharField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_desc = models.CharField(max_length=255, null=True)
    last_login_ip = models.CharField(max_length=255, null=False, default='127.0.0.1')
    now_ip = models.CharField(max_length=255, null=False, default='127.0.0.1')
    u_time = models.DateTimeField(auto_now=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'username'
    
    objects = UserManager()
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def get_now_ip(self):
        return self.now_ip
    
    class Meta:
        ordering = ['pk']


# 操作日志
class Logs(models.Model):
    """
     act_name:操作
     add_time:操作时间
     act_user:操作帐号
     act_content:操作描述
    """
    act_name = models.CharField(max_length=50, null=False, default=None)
    act_user = models.CharField(max_length=20)
    act_content = models.CharField(max_length=255, null=False, default=None)
    add_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # 时间逆序排序
        ordering = ['-add_time']
