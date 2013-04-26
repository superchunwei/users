# -*- coding: utf-8 -*-
import os, time
from django import forms
from codepku.users.models import User
from datetime import datetime 

class SignUpForm(forms.Form):
    """
    注册表单
    fields:
        name email password gender birth work
    """
    name = forms.CharField(max_length=20, label='用户名')
    email = forms.EmailField(label='邮箱地址')
    password = forms.CharField(widget=forms.PasswordInput(),
            label='密码')
    re_password = forms.CharField(widget=forms.PasswordInput(),
            label='重复')
    gender = forms.ChoiceField(label='性别',
        choices=(
            ('male', '男'),
            ('female', '女'),
        ))
    birth = forms.DateTimeField(label='生日')
    work = forms.CharField(label='工作', widget=forms.Textarea)

class LoginForm(forms.Form):
    """
    登陆表单
    """
    name = forms.CharField(max_length=20, label='用户名')
    password = forms.CharField(widget=forms.PasswordInput())


class UserSignUp(object):
    @staticmethod
    def exists(username):
        try:
            user = User.objects.get(name=username)
        except:
            user = None
        return bool(user)

    @staticmethod
    def store(request):
        """
        Store information to database
        """
        post = request.POST
        regist_time = datetime.now()
        # TODO generate new key
        grade = 1
        status = 1
        score = 0
        reset_key = 'KEY'
        open_id = 'OPEN_ID'
        open_token = 'OPEN_TOKEN'
        open_type = 'OPEN_TYPE'
        user = User(
            name = post['name'],
            email = post['email'],
            password = post['password'],
            gender = post['gender'],
            birth = post['birth'],
            work = post['work'],
            regist_time = regist_time,
            grade = grade,
            status = status,
            score = score,
            reset_key = reset_key,
            open_id = open_id,
            open_token = open_token,
            open_type = open_type,
        )
        user.save()
        return user.id
    

def create_validate_key(username, secret_key):
    """
    在首页发送邮件确认点击时生成
    """
    import hashlib
    sha1 = hashlib.sha1
    rand = os.urandom(16)
    now = time.time()
    validate_key = sha1("%s%s%s%s" %(rand, now, username, secret_key))
    return validate_key



def user_info_context(request):
    """
    返回 userid 及 登陆框
    用于登陆
    """
    userid = request.session.get('userid', '')
    username = request.session.get('username', '')
    return {
            'user': {
                'id': userid,
                'name':username,
            },
            'login_form': LoginForm()
    }
