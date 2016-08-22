from django.conf.urls import url
from battle.views import *

urlpatterns = [
    url(r'^home/$', Home.as_view()),
    url(r'^battle/$', Battle.as_view()),
    url(r'^new_battle/$', NewBattle.as_view()),
    url(r'^profile/$', Profile.as_view()),
]
