from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^survey/', views.survey, name="group-ultimatums-survey"),
    url(r'^tutorial/', views.tutorial, name="group-ultimatums-tutorial"),
    url(r'^waiting-room/', views.waiting_room, name="group-ultimatums-waiting"),
    url(r'^group-ultimatum-part-1/', views.game_initial, name="group-ultimatums-game-1"),
    url(r'^group-ultimatum-part-2/', views.game_voting, name="group-ultimatums-game-2"),
    url(r'^group-ultimatum-part-3/', views.game_final, name="group-ultimatums-game-3"),
]
