from django.conf.urls import url, include
from users.views import *

urlpatterns = [
    # url(r'^login/',
    #     'django.contrib.auth.views.login',
    #     {'template_name': 'users\login.html'},
    #     name="login"
    # ),
    url(r'^login/', user_login, name='login'),
    url(r'^signup/', signup, name="signup"),
    url(r'^detail_message/', detail_message, name='detail_message'),
    url(r'^list/', user_list, name='user_list'),
    url(r'^change_code/', change_code, name='change_code'),
    url(r'^user_repeat_ajax/', user_repeat_ajax, name='user_repeat_ajax'),
    url(r'^user_delete_ajax/', user_delete_ajax, name='user_delete_ajax'),
    url(r'^logout/', user_logout, name='logout'),
]
