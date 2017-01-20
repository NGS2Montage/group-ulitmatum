from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^survey/', views.survey, name="public-goods-survey"),
    url(r'^tutorial/', views.tutorial, name="public-goods-tutorial"),
    url(r'^waiting-room/', views.waiting_room, name="public-goods-waiting"),
    url(r'^public-goods/', views.game, name="public-goods-game"),
]
