from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'letter'

urlpatterns = [
    path('writeToMe/', views.writeToMe, name='writeToMe'),
    path('writeToOthers/', views.writeToOthers, name='writeToOthers'),
    path('letterFrmMe/', views.letterFrmMe, name='letterFrmMe'),                                                                                       
    path('letterFrmOthers/', views.letterFrmOthers, name='letterFrmOthers'),
    path('receive/detail/<int:letterId>/', views.recvletter_detail, name='recvletter_detail'),
    path('send/detail/<int:letterId>/', views.sentletter_detail, name='sentletter_detail'),
    path('letterIsent/', views.letterIsent, name='letterIsent'),
    path('delsend/<int:letterId>',views.letter_delete_send,name='letter_delete_send'),
    path('delreceive/<int:letterId>',views.letter_delete_receive, name='letter_delete_receive'),

    path('trash/',views.show_delete_list, name='show_delete_list')
    
]