from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import validUsername, validEmail


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
        
    def clean(self):
        cd = self.cleaned_data
        username = cd.get("username")
        email = cd.get("email")

        try:
            validUsername(username)
        except Exception as e:
            raise forms.ValidationError({"username": e})

        try:
            validEmail(email)
        except  Exception as e:
            raise forms.ValidationError({"email": e})

        return cd