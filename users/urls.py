from django.conf.urls import url, include
from users.views import *

urlpatterns = [
    url(r'^login/',
        'django.contrib.auth.views.login',
        {'template_name': 'users\login.html'},
        name="login"
    ),
    url(r'^signup/', signup, name="signup"),
    url(r'^detail_message/', detail_message, name='detail_message'),
    url(r'^list/', UserListView.as_view(), name='user_list'),
]
