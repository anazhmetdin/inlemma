from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


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

        if re.compile(r'.*[@\.\+-]',).match(username) != None:
            raise forms.ValidationError({"username": "Username contains invalid characters"})
        
        elif len(username) > 16 or len(username) < 4:
            raise forms.ValidationError({"username": "Username length is outside the range"})

        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError({"username": f'Username "{username}" is not available'})

        return cd