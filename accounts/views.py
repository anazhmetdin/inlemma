from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms.utils import ErrorList
from .forms import NewUserForm
from django.contrib import messages
from django.views import View


class loginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
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
            messages.error(request, ErrorList(["Wrong username or password."]))
            return redirect('login')

class logoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class registerView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {'form': NewUserForm()}
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, ErrorList(["Registration successful."]) )
            return redirect("home")
        for error in form.errors:
            messages.error(request, form.errors[error])
            print(type(form.errors[error]))
        return redirect('register')