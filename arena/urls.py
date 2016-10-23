"""arena URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='index'),
    url(r'^new/$', views.NewView.as_view(), name='new'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^accounts/', include('allauth.urls'), name='login'),
    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^@(?P<username>\w+)$', views.UserView.as_view(), name='user_profile'),
    url(r'^(?P<fighter_slug>\w+)/$', views.FighterView.as_view(), name='fighter_profile'),
    url(r'^(?P<fighter_slug>\w+)/edit/$', views.FighterView.as_view(), name='fighter_edit'),
    url(r'^(?P<slug_one>\w+)/(?P<slug_two>\w+)/$', views.BattleView.as_view(), name='battle_page'),
]
