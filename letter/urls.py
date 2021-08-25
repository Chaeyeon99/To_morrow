from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'letter'

urlpatterns = [
    path('writeToMe/', views.writeToMe, name='writeToMe'),
    path('writeToOthers/', views.writeToOthers, name='writeToOthers'),
    # path('to_me/', views.to_me, name='to_me'),
    path('letterFrmMe/', views.letterFrmMe, name='letterFrmMe'),                                                                                       
    path('letterFrmOthers/', views.letterFrmOthers, name='letterFrmOthers'),
    path('receive/detail/<int:letterId>/', views.recvletter_detail, name='recvletter_detail'),
    path('send/detail/<int:letterId>/', views.sentletter_detail, name='sentletter_detail'),
    path('letterIsent/', views.letterIsent, name='letterIsent'),
    
]