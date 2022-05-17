from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View


class loginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.error(request, ("Wrong username or password"))
            return redirect('login')

class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')