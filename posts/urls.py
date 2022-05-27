from django.urls import path
from . import views

urlpatterns = [
    path('<pid>', views.postView.as_view(), name='post'),
    path('comment/<pid>', views.commentView.as_view(), name='comment'),
]