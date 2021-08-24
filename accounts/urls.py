from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


app_name = 'accounts'

urlpatterns = [
    path('', views.Index, name='Index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('update', views.updateProfile, name='update'),
    path('password', views.password, name='password'),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html', success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'
    ),
    path('password_reset_done/', 
    auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete'), template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    
    # path('password_reset_confirm/<uidb64>/<token>/',	auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),




]