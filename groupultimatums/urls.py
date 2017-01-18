from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^waiting-room/', views.waiting_room),
    url(r'^group-ultimatum-part-1/', views.game_initial),
    url(r'^group-ultimatum-part-2/', views.game_voting),
    url(r'^group-ultimatum-part-3/', views.game_final),
]
