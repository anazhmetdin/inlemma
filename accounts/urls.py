from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginView.as_view(), name='login'),
    path('logout', views.logoutView.as_view(), name='logout'),
    path('register', views.registerView.as_view(), name='register'), 
    path('activate/<uidb64>/<token>', views.activateView.as_view(), name='activateGET'),
    path('activate', views.activateView.as_view(), name='activatePOST'),   
]