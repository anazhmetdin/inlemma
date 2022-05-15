from django.urls import include, path, reverse
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="home/landing.html")),
    path('accounts/', include('django.contrib.auth.urls'))
]