# -*- coding: utf-8 -*-
"""
用户信息操作
如: 注册 注销 登陆等
"""

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from control import SignUpForm, UserSignUp, LoginForm
from django.views.generic import TemplateView
from codepku.users.models import User
from codepku.utils import tojson


class SignUp(TemplateView):
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            UserSignUp.store(request)
            return tojson({'signup':True})
        else:
            return tojson({'signup':False, 
                    'message':'请正确填写表格'})

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, "users/signup_dy.tpl" , 
                { 'form': form, })
        

def exists(request):
    """
    Does this user exists?
    args:
        request.POST['username']

    returns:
        json: {'exists':true/false}
    """
    res = {'exists':True}
    username = request.POST.get('username', '')
    if not username:
        return tojson(res)
    else:
        res['exists'] = UserSignUp.exists(username)
    return tojson(res)

def reset_pwd(request, username, valid_key):
    """
    request resert_password_url
    """
    try:
        _user = User.objects.get(name=username)
        # TODO reset_key?
        if valid_key == _user.reset_key:
            return True
    except:
        pass
    return False
