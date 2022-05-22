from django.shortcuts import redirect, render
from django.views import View

class homeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.profile.mail_activated or not request.user.has_usable_password():
                return render(request, 'home/homespace.html')
            else:
                return render(request, 'home/activate.html')
        else:
            return render(request, 'home/landing.html')
