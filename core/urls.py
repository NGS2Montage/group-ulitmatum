from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_login, name='login_user'),
    url(r'^login/$', views.user_login, name='login_user'),
    url(r'^login$', views.user_login, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^logout$', views.logout_user, name='logout_user'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^create_account$', views.create_account, name='create_account'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
    url(r'^forgot_password$', views.forgot_password, name='forgot_password'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^change_password$', views.change_password, name='change_password'),
]
