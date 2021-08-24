from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'letter'

urlpatterns = [
    path('emotion_result/', views.emotion_result, name='emotion_result'),
    path('writeToMe/', views.writeToMe, name='writeToMe'),
     path('writeToOthers/', views.writeToOthers, name='writeToOthers'),
    path('receive/', views.receive, name='receive'),
    path('to_me/', views.to_me, name='to_me'),
    path('<int:letter_id>/', views.message_detail, name='message_detail'), #목록보기 밑에 들어가야할 것 같은데...
]