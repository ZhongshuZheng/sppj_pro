from django.conf.urls import url, include

urlpatterns = [
    url(r'^login/',
        'django.contrib.auth.views.login',
        {'template_name': 'user.login.html'}
    ),
]
