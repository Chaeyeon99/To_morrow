from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.Index, name='Index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update', views.updateProfile, name='update'),
    path('password', views.password, name='password'),
]