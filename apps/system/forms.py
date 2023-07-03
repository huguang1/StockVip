from django import forms
from utils.forms import FormMixin

from .models import User


class LoginForm(forms.Form, FormMixin):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)
    img_captcha = forms.CharField(max_length=4, min_length=4)
    img_code_id = forms.CharField(max_length=255)


class ChangAllPwdForm(forms.Form, FormMixin):
    """
    'oldpwd': oldPwd,
    'newpwd1': newPwd,
    'newpwd2': newPwd2
    """
    user_id = forms.CharField(max_length=255)
    newpwd1 = forms.CharField(max_length=255)
    newpwd2 = forms.CharField(max_length=255)
    
    def clean(self):
        cleaned_data = super(ChangAllPwdForm, self).clean()
        
        pwd1 = cleaned_data.get('newpwd1')
        pwd2 = cleaned_data.get('newpwd1')
        
        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致')
        
        return cleaned_data


class ChangPwdForm(forms.Form, FormMixin):
    """
    'oldpwd': oldPwd,
    'newpwd1': newPwd,
    'newpwd2': newPwd2
    """
    oldpwd = forms.CharField(max_length=255)
    newpwd1 = forms.CharField(max_length=255)
    newpwd2 = forms.CharField(max_length=255)
    
    def clean(self):
        cleaned_data = super(ChangPwdForm, self).clean()
        
        pwd1 = cleaned_data.get('newpwd1')
        pwd2 = cleaned_data.get('newpwd1')
        
        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致')
        
        return cleaned_data


class RegisterForm(forms.Form, FormMixin):
    """
    'username': username,
    'pwd1': pwd1,
    'pwd2': pwd2,
    'desc': userDesc,
    'type': user_type,
    'activation': activation
    """
    username = forms.CharField(max_length=255)
    pwd1 = forms.CharField(max_length=255)
    pwd2 = forms.CharField(max_length=255)
    desc = forms.CharField(max_length=255)
    user_type = forms.IntegerField(max_value=1, min_value=0)
    activation = forms.IntegerField(max_value=1, min_value=0)
    
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        
        pwd1 = cleaned_data.get("pwd1")
        pwd2 = cleaned_data.get("pwd2")
        
        if pwd1 != pwd2:
            raise forms.ValidationError('两次密码不一致')

        username = cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('该用户名已经被注册！')
       
        return cleaned_data
