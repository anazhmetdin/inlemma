from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.forms.utils import ErrorList
from django.views import View
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode
from .utils import sendConfirmationMail, ConfirmationTokenGenerator, emailIsValid

class loginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {'form': AuthenticationForm()}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        
        # Return an 'invalid login' error message.
        if form.errors:
            for error in form.errors:
                messages.error(request, form.errors[error])
        else:
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
            sendConfirmationMail(request, user)
            return redirect("home")
        
        for error in form.errors:
            messages.error(request, form.errors[error])
        
        return redirect('register')


class activateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None
        
        if user and ConfirmationTokenGenerator().check_token(user, token):
            user.profile.mail_activated = True
            user.save()
            messages.success(request, ErrorList(["Email confirmed."]) )
        else:
            messages.error(request, ErrorList(["Invalid link."]) )
        
        return redirect('home')

    def post(self, request):
        if request.user.email == '':
            email = request.POST.get('email')
            if not emailIsValid(email):
                messages.error(request, ErrorList(["Invalid email address."]) )
                return redirect('home')
            else:
                request.user.email = email
                request.user.save()

        sendConfirmationMail(request, request.user)
        messages.success(request, ErrorList(["Email sent, please check your inbox."]) )

        return redirect('home')
