from django.conf.urls.defaults import *
from views import *
from views.userinfo import *

import os
APP_PATH = os.path.dirname(__file__)
static_path = os.path.join(APP_PATH, 'static')

urlpatterns = patterns('',
    url(r'^signup$', SignUp.as_view()),
    url(r'^login$', Login.as_view(), name='login'),
    url(r'^exists$', exists),
    url(r'^logout$', logout),
    url(r'^userinfo$', UserInfoPage.as_view()),
)
