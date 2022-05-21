from xml.dom import ValidationErr
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.forms.utils import ErrorList
from django.views import View
from django.utils.encoding import  force_str
from django.utils.http import urlsafe_base64_decode
from .utils import sendMail, ConfirmationTokenGenerator, emailIsValid, validEmail
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class loginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        context = {'form': AuthenticationForm()}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        print(form.data)
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
            sendMail(request, request.user,
                     'Confirm your email', 'accounts/confirmation.html',
                     ConfirmationTokenGenerator)
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
            if not user.profile.mail_activated:
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
                try:
                    validEmail(email)
                except Exception as e:
                    messages.error(request, ErrorList(["This email is linked to another account."]) )
                    return redirect('home')
                request.user.email = email
                request.user.save()

        sendMail(request, request.user,
                 'Confirm your email', 'accounts/confirmation.html',
                 ConfirmationTokenGenerator)
        messages.success(request, ErrorList(["Email sent, please check your inbox."]) )

        return redirect('home')


class passwordChangeView(View):
    def get(self, request):
        if request.user.social_auth.exists():
            messages.error(request,  ErrorList(["This account was registered using external authentication, please login using the same method."]))
            return redirect('login')
        context = {'form': PasswordChangeForm(request.user)}
        return render(request, 'accounts/passwordChange.html', context)

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,  ErrorList(["Password changed succesfully."]))
            return redirect('home')
        else:
            for error in form.error_messages:
                messages.error(request,  ErrorList([form.error_messages[error]]))
            return redirect('passwordChange')


class passwordResetFormView(View):
    def get(self, request):
        context = {'form': PasswordResetForm()}
        return render(request, 'accounts/passwordResetForm.html', context)

    def post(self, request):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST.get('email'))
            if user.social_auth.exists():
                messages.error(request,  ErrorList(["This account was registered using external authentication, please login using the same method."]))
                return redirect('login')
            sendMail(request, user,
                     'Password reset', 'accounts/passwordResetLink.html',
                     PasswordResetTokenGenerator, )
            messages.success(request,  ErrorList(["A password reset link was sent out."]))
            return redirect('home')
        else:
            return redirect('passwordChange')


class passwordResetView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except:
            user = None
        
        if user and PasswordResetTokenGenerator().check_token(user, token):
            context = {'form': SetPasswordForm(user)}
            return render(request, 'accounts/passwordReset.html', context)
        else:
            messages.error(request, ErrorList(["Invalid link."]) )
        
        return redirect('home')
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
        except Exception as e:
            return redirect('home')

        user = User.objects.get(id=uid)
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])  
            user.save()      
            update_session_auth_hash(request, user)
            messages.success(request,  ErrorList(["Password changed succesfully."]))
            return redirect('home')
        else:
            for error in form.error_messages:
                messages.error(request,  ErrorList([form.error_messages[error]]))
            return redirect('passwordReset', uidb64=uidb64, token=token)