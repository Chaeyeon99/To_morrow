from django.conf.urls import url
from django.urls import path, include
from . import views

app_name = 'letter'

urlpatterns = [
    path('writeToMe/', views.writeToMe, name='writeToMe'),
    path('writeToOthers/', views.writeToOthers, name='writeToOthers'),
    path('to_me/', views.to_me, name='to_me'),
    path('letterFrmOthers/', views.letterFrmOthers, name='letterFrmOthers'),
    path('<int:letterId>/', views.letter_detail, name='letter_detail.html'), #목록보기 밑에 들어가야할 것 같은데...
]