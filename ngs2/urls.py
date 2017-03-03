"""ngs2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from core import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redirect/$', views.MyRedirectView.as_view(), name='redirect'),
    url(r'^oops/$', TemplateView.as_view(template_name='oops.html'), name='oops'),
    url(r'^additional_user_info/$', TemplateView.as_view(template_name='additional_user_info.html'), name='additional-user-info'),
    url(r'^initial_survey/$', TemplateView.as_view(template_name='initial_survey.html'), name='initial-survey'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^phase1/', include('anagrams.urls')),
    url(r'^phase2/', include('publicgoods.urls')),
    url(r'^phase3/', include('groupultimatums.urls')),
    url(r'^state-mismatch/', views.state_mismatch, name='state-mismatch')
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
