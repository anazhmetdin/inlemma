from re import template
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login', views.loginView.as_view(), name='login'),
    path('logout', views.logoutView.as_view(), name='logout'),
    path('register', views.registerView.as_view(), name='register'), 
    path('activate/<uidb64>/<token>', views.activateView.as_view(), name='activateGET'),
    path('activate', login_required(views.activateView.as_view()), name='activatePOST'),
    path('password/change', login_required(views.passwordChangeView.as_view()), name='passwordChange')
]