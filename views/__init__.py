# -*- coding: utf-8 -*-
__all__ = (
    'exists', 'reset_pwd',
    'Login', 'SignUp', 'logout',
)


from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from control import SignUpForm, UserSignUp, LoginForm
from django.views.generic import TemplateView
from codepku.users.models import User
from codepku.utils import tojson


from useraction import exists, reset_pwd, SignUp
from userinfo import *


class Login(TemplateView):

    template_name = "users/login_dy.tpl"

    def post(self, request, *args, **kwargs):
        """
        用户注册
        args:
            username, password
        return:
            json:
            { login: true/false, userid: 2, message:'wrong?'}
        """
        # 提交登陆信息
        username = request.POST.get('name', '')
        password = request.POST.get('password', '')
        res = {'login':False, 'userid':-1, 'username': username}
        if username and password:
            try:
                user = User.objects.get(name=username)
                if user.password == password: 
                    res['login'] = True
                    res['userid'] = user.id
                    request.session['userid'] = res['userid']
                    request.session['username'] = res['username']
            except:
                pass
        return tojson(res)

    def get(self, request, *args, **kwargs):
        # 访问页面
        form = LoginForm()
        return render(request, "users/login_dy.tpl" , 
                    { 'form': form })

def logout(request):
    """
    return:
        json: {'logout':true}
    """
    try:
        del request.session['userid']
    except KeyError:
        pass

    try:
        del request.session['username']
    except KeyError:
        pass
    res = {'logout':True}
    return tojson(res)


