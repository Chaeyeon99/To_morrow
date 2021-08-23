from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Index, name='Index'),
    path('SignUp/', views.SignUp, name='SignUp'),
]