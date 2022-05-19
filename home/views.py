from django.shortcuts import redirect, render
from django.views import View

class homeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'home/homespace.html')
        else:
            return render(request, 'home/landing.html')
