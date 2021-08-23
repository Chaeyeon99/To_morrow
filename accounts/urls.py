from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Index, name='Index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]