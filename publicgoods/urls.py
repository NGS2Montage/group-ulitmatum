from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^waiting-room/', views.waiting_room),
    url(r'^public-goods/', views.game),
]
