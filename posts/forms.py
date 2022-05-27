from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm
from .models import Post, Comment

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
        model = Post
        fields = ['anonymous', 'comments', 'messages', 'title', 'body']


class CommentForm(ModelForm):
    
    def __init__(self, user=None, post=None, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        self.post = post

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  
        instance.post = self.post        
        instance.save(commit)
        return instance


    class Meta:
        model = Comment
        fields = ['anonymous', 'body']