from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from .models import post

class PostForm(ModelForm):
    
    def __init__(self, user=None, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.published = 'publish' in self.data            
        instance.save(commit)
        return instance


    class Meta:
        model = post
        fields = ['anonymous', 'comments', 'messages', 'HTML', 'title', 'body']